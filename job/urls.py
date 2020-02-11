from django.urls import path
from django.views.generic import TemplateView
from job.api import *
urlpatterns = [
    path('', TemplateView.as_view(template_name='post-job.html')),
    path('job-list', TemplateView.as_view(template_name='company-list.html')),
    path('company/', CompanyList.as_view()),
    path('industry/', IndustryList.as_view()),
    path('job_type/', JobTypeList.as_view()),
    path('experience/', ExperienceList.as_view()),
    path('qualification/', QualificationList.as_view()),
    path('gender/', GenderList.as_view()),
    path('job_update/<str:pk>/', JobUpdateView.as_view()),
    # path('add', TemplateView.as_view(template_name='company-create.html')),
    # path('list', TemplateView.as_view(template_name='company-list.html')),
    # path('update', TemplateView.as_view(template_name='company-update.html')),
    # path('details', TemplateView.as_view(template_name='job-details.html')),
    path('job_create/', job_create),

]