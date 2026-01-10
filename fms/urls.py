"""
URL configuration for fms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from faculty import views
from django.contrib.auth.views import *
from django.conf import settings
from django.conf.urls.static import static
from faculty.forms import CustomLoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('contact/',views.contact,name='contact'),
    path('register/', views.register, name='register'),
    path('login/',LoginView.as_view(template_name="faculty/login.html",redirect_authenticated_user=True,form_class=CustomLoginForm),name="login"),
    path("logout/",views.logout_user,name='logout'),
    path("<str:faculty>/",include("faculty.urls")),
    # path('logout/',views.logout,name="logout"),
    path('password-reset/',PasswordResetView.as_view(template_name="faculty/password_reset.html"),name="password_reset"),
    path('password-reset/success/',PasswordResetDoneView.as_view(template_name="faculty/password_reset_done.html"),name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name="faculty/password_reset_confirm.html"),name="password_reset_confirm"),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name="faculty/password_reset_complete.html"),name="password_reset_complete"),
    path('confirm-email-change/<uidb64>/<token>/',views.confirm_email_change,name="confirm_email_change"),
    path('allfaculty/',views.all_faculty,name="all_faculty"),
    path('<username>/all-documents/', views.view_all_documents, name='view_all_documents'),
    path('download-research-report/', views.download_research_report, name='download_research_report'),
    path('download-achievements-report/', views.download_achievements_report, name='download_achievements_report'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
