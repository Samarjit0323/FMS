from django.urls import path
from .views import *

urlpatterns=[
    path("dashboard/",dashboard,name="dashboard"),
    path("profile/",view_profile,name="view_profile"),
    path("update_profile/",update_profile,name="update_profile"),
]

