from django.urls import path
from django.views.generic import TemplateView
from job.api import *
urlpatterns = [
    path('job', CompanyList.as_view()),
]