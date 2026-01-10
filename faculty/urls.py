from django.urls import path
from .views import *
from django.contrib.auth.views import *

urlpatterns=[
    path("dashboard/",dashboard,name="dashboard"),
    path("profile/",view_profile,name="view_profile"),
    path("update_profile/",update_profile,name="update_profile"),
    path('change-email/',request_email_change,name='request_email_change'),
    path('personal_docs/',personal_docs,name="personal_docs"),
    path('assignments/',assignments,name="assignments"),
    path('research/',research,name="research"),
    path('personal_docs/<int:doc_id>/delete/',delete_pdoc,name="delete_pdoc"),
    path('assignments/<int:doc_id>/delete/',delete_assignments,name="delete_assignments"),
    path('research/<int:doc_id>/delete/',delete_research,name="delete_research"),
    path('achievements/',achievements,name="achievements"),
    path('achievements/<int:achievement_id>/delete/',delete_achievement,name="delete_achievement"),
]