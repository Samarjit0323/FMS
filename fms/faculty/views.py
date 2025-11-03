from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import FacultyProfile
from .forms import ProfileUpdationForm, RegisterForm

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

