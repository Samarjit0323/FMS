from django import forms
from django.contrib.auth import models
from .models import FacultyProfile, PersonalDocs, AssignmentDocs, ResearchPublications
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.bootstrap import AppendedText
from .validators import validate_file, validate_image
from cloudinary.forms import CloudinaryJsFileField

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.helper=FormHelper()
        self.helper.form_tag=False
        self.helper.layout=Layout(
            'username',
            AppendedText(
                Field('password',id="id_password"),
                '<i id="togglePassword" class="bi bi-eye" style="cursor: pointer;"></i>'
            )
        )

DEPARTMENT_CHOICES = (
    ("", "Select department"),
    ("CSE", "Computer Science & Engineering"),
) #as of now only one dept

class RegisterForm(UserCreationForm):
    email=forms.CharField(max_length=100)
    class Meta:
        model=models.User
        fields=['username','first_name','last_name','email','password1','password2']
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['first_name'].help_text="Include Title(Dr., Prof., Asst. Prof. etc) and Middle Name if applicable"
        self.fields['email'].help_text="Email ID will be visible to Admin"
        self.fields['first_name'].required=True
        self.fields['last_name'].required=True

class ProfileUpdationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True,help_text="Include Title(Dr., Prof., Asst. Prof. etc) and Middle Name if applicable")
    last_name = forms.CharField(max_length=150, required=True)
    # image = CloudinaryJsFileField(required=False)
    class Meta:
        model=FacultyProfile
        exclude=('user',)

    def __init__(self, *args, **kwargs):
        # Pop the user object from the view
        user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
        if self.instance and self.instance.image:
             self.fields['image'].initial = self.instance.image
        self.fields['image'].required = False
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'department',
            'designation',
            'phone',
            'address',
            'image'
        )
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            validate_image(image)
        return image

class EmailUpdateForm(forms.Form):
    email=forms.EmailField(label="New Email Address",required=True,help_text="A verification link will be sent to this new email address.")

    def clean_email(self):
        new_email=self.cleaned_data.get('email')
        if models.User.objects.filter(email=new_email).exists():
            raise forms.ValidationError("This email ID is already in use")
        return new_email
    
class UploadPDForm(forms.ModelForm):

    class Meta:
        model=PersonalDocs
        exclude=('faculty',)
        widgets = {
            'doc': forms.ClearableFileInput(attrs={
                'accept': '.pdf, .jpg, .jpeg, .png'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['doc'].help_text="Upload only .pdf files"
        self.fields['title'].help_text="Brief one line description of uploading document"

    def clean_doc(self):
        file = self.cleaned_data.get('doc')
        if file:
            validate_file(file)
        return file

class UploadAssignmentForm(forms.ModelForm):
    class Meta:
        model=AssignmentDocs
        exclude=('faculty',)
        widgets = {
            'file': forms.ClearableFileInput(attrs={
                'accept': '.pdf, .jpg, .jpeg, .png'
            }),
            'date_of_submission': forms.TextInput(
                attrs={
                    'class': 'datepicker', 
                    'placeholder': 'Click to select a date...'
                }
            ),
            'date_of_assignment': forms.TextInput(
                attrs={
                    'class': 'datepicker', 
                    'placeholder': 'Click to select a date...'
                }
            )
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['file'].help_text="Accepted extensions: .pdf, .jpg, .jpeg, .png"
        self.fields['title'].help_text="Brief one line description of uploading assignment"

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            validate_file(file)
        return file

class UploadResearchForm(forms.ModelForm):
    class Meta:
        model=ResearchPublications
        exclude=('faculty',)
        widgets = {
            'publication_date': forms.TextInput(
                attrs={
                    'class': 'datepicker', 
                    'placeholder': 'Click to select a date...'
                }
            )
        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['title'].help_text="Title of Research Publication"
        self.fields['link'].help_text="Link of publication"
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            validate_file(file)
        return file