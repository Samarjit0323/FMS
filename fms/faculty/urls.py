from django.urls import path
from .views import *
from django.contrib.auth.views import *

urlpatterns=[
    path("dashboard/",dashboard,name="dashboard"),
    path("profile/",view_profile,name="view_profile"),
    path("update_profile/",update_profile,name="update_profile"),
    path('change-email/',request_email_change,name='request_email_change')
]