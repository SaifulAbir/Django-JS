from django.urls import path
from django.views.generic import TemplateView
from job.api import *
urlpatterns = [
    path('company', CompanyList.as_view()),
]