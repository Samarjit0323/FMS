from django.contrib import admin
from .models import FacultyProfile,PersonalDocs, AssignmentDocs, ResearchPublications

# Register your models here.
admin.site.register(FacultyProfile)
admin.site.register(PersonalDocs)
admin.site.register(AssignmentDocs)
admin.site.register(ResearchPublications)