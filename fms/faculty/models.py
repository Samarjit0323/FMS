from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class FacultyProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    department=models.CharField(default="Computer Science & Engineering",max_length=50)
    designation=models.CharField(max_length=50)
    image=models.ImageField(upload_to="profile_pics",default="profile_pics/default_profile.jpg")
    phone=models.CharField(max_length=13,blank=True)
    address=models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}, {self.designation}, {self.department}"

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        if self.image:
            img=Image.open(self.image.path)
            if img.height>300 or img.width>300:
                output_size=(300,300)
                img.thumbnail(output_size)
                img.save(self.image.path)