from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
import os
from django.core.exceptions import ValidationError
# Create your models here.

def validate_file_type(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    if ext not in valid_extensions:
        raise ValidationError('Unsupported file type. Allowed types: PDF, JPG, JPEG, PNG.')
    
class FacultyProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    department=models.CharField(default="Computer Science & Engineering",max_length=50)
    designation=models.CharField(max_length=50)
    image=models.ImageField(upload_to="profile_pics",default="profile_pics/default_profile.jpg")
    phone=models.CharField(max_length=13,blank=True)
    address=models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}, {self.designation}, {self.department}"

    # def save(self,*args,**kwargs):
    #     super().save(*args,**kwargs)
    #     if self.image:
    #         img=Image.open(self.image.path)
    #         if img.height>300 or img.width>300:
    #             output_size=(300,300)
    #             img.thumbnail(output_size)
    #             img.save(self.image.path)

class PersonalDocs(models.Model):
    faculty=models.ForeignKey(FacultyProfile,on_delete=models.CASCADE,related_name="personal_docs")
    doc=models.FileField(upload_to="docs/personal_docs/",validators=[validate_file_type])
    title=models.CharField(max_length=100)
    uploaded_on=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} (Uploaded on {self.uploaded_on})"
    
class AssignmentDocs(models.Model):
    faculty=models.ForeignKey(FacultyProfile,on_delete=models.CASCADE,related_name='assignments')
    file=models.FileField(upload_to="docs/assignments/",validators=[validate_file_type])
    title=models.CharField(max_length=100)
    uploaded_on=models.DateTimeField(default=timezone.now)
    date_of_assignment=models.DateField()
    date_of_submission=models.DateField()

    def __str__(self):
        return f"{self.title} (DOA: {self.date_of_assignment}; DOS: {self.date_of_submission})"
    
class ResearchPublications(models.Model):
    faculty=models.ForeignKey(FacultyProfile,on_delete=models.CASCADE,related_name="research")
    file=models.FileField(upload_to="docs/research")
    title=models.CharField(max_length=100)
    subject=models.CharField(max_length=50,default="NA")
    publication_date=models.DateField()
    link=models.URLField()

    def __str__(self):
        return f"{self.title} ({self.subject})"