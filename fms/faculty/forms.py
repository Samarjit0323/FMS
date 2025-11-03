from django import forms
from django.contrib.auth import models
from .models import FacultyProfile
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

DEPARTMENT_CHOICES = (
    ("", "Select department"),
    ("CSE", "Computer Science & Engineering"),
) #as of now only one dept

class RegisterForm(UserCreationForm):
    email=forms.CharField(max_length=100)
    class Meta:
        model=models.User
        fields=['username','first_name','last_name','email','password1','password2']

class ProfileUpdationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
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