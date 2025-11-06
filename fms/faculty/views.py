from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import FacultyProfile, PersonalDocs
from .forms import ProfileUpdationForm, RegisterForm, EmailUpdateForm,UploadPDForm
from django.conf import settings
#token generator and email tools
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.base import ContentFile
from pypdf import PdfReader, PdfWriter
import os, io

def home(request):
    return render(request, 'faculty/base.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f"{username} registered successfully! Login to access Dashboard")
            return redirect('login')
    else:
        form=RegisterForm()
    return render(request, 'faculty/register.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request,"You have been logged out. Click on login to revisit.")
    return redirect('home')

@login_required
def dashboard(request,faculty):
    try:
        faculty_profile=FacultyProfile.objects.get(user=request.user)
    except FacultyProfile.DoesNotExist:
        messages.warning(request,"Update profile to access dashboard")
        return redirect('update_profile')
    return render(request,"faculty/dashboard.html",{"faculty":faculty_profile})

@login_required
def update_profile(request,faculty):
    try:
        faculty_profile=FacultyProfile.objects.get(user=request.user)
    except FacultyProfile.DoesNotExist:
        faculty_profile=None
    if request.method=="POST":
        form=ProfileUpdationForm(request.POST, request.FILES, instance=faculty_profile)
        if form.is_valid():
            faculty_profile=form.save(commit=False)
            faculty_profile.user=request.user
            faculty_profile.save()

            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()

            messages.success(request,"Profile updated successfully!")
            return redirect('dashboard',faculty=request.user.username)
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        }
        form=ProfileUpdationForm(instance=faculty_profile,initial=initial_data)
    return render(request,'faculty/update_profile.html',{'form':form,'faculty':faculty_profile})

@login_required
def view_profile(request,faculty):
    faculty_profile=get_object_or_404(FacultyProfile,user=request.user)
    return render(request, 'faculty/view_profile.html',{'faculty':faculty_profile})

@login_required
def request_email_change(request,faculty):
    try:
        faculty= FacultyProfile.objects.get(user=request.user)
    except FacultyProfile.DoesNotExist:
        return redirect('dashboard', faculty=user.username)
    if request.method=="POST":
        # print("DEBUG: request.POST ->", request.POST)
        form=EmailUpdateForm(request.POST)
        if form.is_valid():
            new_email=form.cleaned_data['email']
            user=request.user
            #uidb64 encodes the user’s primary key (ID) safely in base64 (e.g., "Mg" for user ID 2).
            #token is a time-sensitive hash that expires after some time or when the user changes password — so it can’t be reused.
            token=default_token_generator.make_token(user)
            uidb64=urlsafe_base64_encode(force_bytes(user.pk))

            request.session['pending_email_change']=new_email #it’s not yet applied to the database.
            #The change only takes effect after the user confirms the email through the link.

            current_site=get_current_site(request)
            mail_subject="Confirm your new email address"
            message=render_to_string(
                'email/email_change_link.txt',
                {
                    'user':user,
                    'protocol':'http',
                    'domain':current_site.domain,
                    'uidb64':uidb64,
                    'token':token,
                }
            )

            try:
                send_mail(mail_subject,message,settings.EMAIL_HOST_USER,[new_email])
                messages.success(request,f"A verification link has been sent to {new_email}")
                return redirect('dashboard',faculty=user.username)
            except Exception as e:
                messages.error(request,"Email not delivered. Recheck email address to proceed.")
    else:
        form=EmailUpdateForm()
    return render(request, "faculty/request_email_change.html",{'form':form,'faculty':faculty})

def confirm_email_change(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError, User.DoesNotExist):
        user=None

    new_email=request.session.get('pending_email_change')

    if user is not None and default_token_generator.check_token(user,token) and new_email:
        user.email=new_email
        user.save()
        if 'pending_email_change' in request.session:
            del request.session['pending_email_change']
        messages.success(request,"Email Updated successfully!")
        return redirect('dashboard',faculty=user.username)
    else:
        messages.error(request,"Link is either invalid or has expired.")
        return redirect('home')
    
def contact(request):
    faculty_profiles=FacultyProfile.objects.all()
    return render(request, "faculty/contact.html",{"faculty_profiles":faculty_profiles})

@login_required
def personal_docs(request,faculty):
    if request.user.username != faculty:
        return redirect('personal_docs', faculty=request.user.username)
    try:
        faculty_profile = request.user.facultyprofile
    except FacultyProfile.DoesNotExist:
        messages.error(request, "Faculty profile not found. Please create one.")
        return redirect('update_profile',faculty=request.user.username)
    if request.method=="POST":
        form=UploadPDForm(request.POST,request.FILES)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.faculty=faculty_profile
            uploaded_file=instance.doc
            ext= os.path.splitext(uploaded_file.name)[1].lower()
            if ext==".pdf":
                try:
                    reader=PdfReader(uploaded_file.file)
                    writer=PdfWriter()
                    for page in reader.pages:
                        writer.add_page(page)
                        writer.pages[-1].compress_content_streams()
                    compressed_buffer=io.BytesIO()
                    writer.write(compressed_buffer)
                    compressed_buffer.seek(0)
                    instance.doc=ContentFile(compressed_buffer.read(),name=uploaded_file.name)
                except Exception as e:
                    messages.error(request,e)
                    return render(request, "faculty/personal_docs.html", {"faculty": faculty_profile, "form": form})
            instance.save()
            messages.success(request,"Document has been uploaded successfully!")
            return redirect('personal_docs',faculty=request.user.username)
        else:
            messages.error(request,"Fix Errors in form")
    else:
        form=UploadPDForm()
    docs_list=PersonalDocs.objects.filter(faculty=faculty_profile).order_by("-uploaded_on")
    return render(request,"faculty/personal_docs.html",{"faculty":faculty_profile,"form":form,"docs_list":docs_list})

@login_required
def assignments(request,faculty):
    faculty=FacultyProfile.objects.get(user=request.user)
    return render(request,"faculty/assignments.html",{"faculty":faculty})

@login_required
def research(request,faculty):
    faculty=FacultyProfile.objects.get(user=request.user)
    return render(request,"faculty/research.html",{"faculty":faculty})

@login_required
def delete_pdoc(request,faculty,doc_id):
    document=get_object_or_404(PersonalDocs,id=doc_id)
    if document.faculty.user!=request.user:
        messages.success(request,"Persmission Denied")
        return redirect("personal_docs",faculty=request.user.username)
    doc_title=document.title
    document.delete()
    messages.success(request,f"{ doc_title } deleted successfully!")
    return redirect("personal_docs",faculty=request.user.username)
    
