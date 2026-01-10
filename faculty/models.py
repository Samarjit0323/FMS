from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
import os
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField

def validate_file_type(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    if ext not in valid_extensions:
        raise ValidationError('Unsupported file type. Allowed types: PDF, JPG, JPEG, PNG.')
    
class FacultyProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    department=models.CharField(default="Computer Science & Engineering",max_length=50)
    designation=models.CharField(max_length=50)
    # image=models.ImageField(upload_to="profile_pics",default="profile_pics/default_profile.jpg")
    image=CloudinaryField(folder="profile_pics",default="profile_pics/d6r8kppjwtafmjw5mpup")
    
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
    doc=CloudinaryField(resource_type='raw',folder="docs/personal_docs",validators=[validate_file_type])
    title=models.CharField(max_length=100)
    uploaded_on=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} (Uploaded on {self.uploaded_on})"
    
class AssignmentDocs(models.Model):
    faculty=models.ForeignKey(FacultyProfile,on_delete=models.CASCADE,related_name='assignments')
    file=CloudinaryField(resource_type='raw',folder="docs/assignments",validators=[validate_file_type])
    title=models.CharField(max_length=100)
    uploaded_on=models.DateTimeField(default=timezone.now)
    date_of_assignment=models.DateField()
    date_of_submission=models.DateField()

    def __str__(self):
        return f"{self.title} (DOA: {self.date_of_assignment}; DOS: {self.date_of_submission})"
    
class ResearchPublications(models.Model):
    faculty=models.ForeignKey(FacultyProfile,on_delete=models.CASCADE,related_name="research")
    file=CloudinaryField(resource_type='raw',folder="docs/research")
    title=models.CharField(max_length=100)
    subject=models.CharField(max_length=50,default="NA")
    publication_date=models.DateField()
    link=models.URLField(blank=True)

    def __str__(self):
        return f"{self.title} ({self.subject})"

class Achievements(models.Model):
    faculty=models.ForeignKey(FacultyProfile,on_delete=models.CASCADE,related_name="achievements")
    event=models.CharField(max_length=200)
    date=models.DateField()
    organized_by=models.CharField(max_length=100)
    role_type=models.CharField(max_length=50,choices=[('Participant','Participant'),('Presented Research Paper','Presented Research Paper'),('Keynote Speaker','Keynote Speaker'),('Invited session chair','Invited session chair')],default='Participant')

    def __str__(self):
        return f"{self.event} on {self.date} ({self.role_type})"