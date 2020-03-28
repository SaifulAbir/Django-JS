from django.urls import path
from django.views.generic import TemplateView
from job.api import *
urlpatterns = [
    path('post-job/', TemplateView.as_view(template_name='post-job.html'), name='post_job'),
    path('validation-test', TemplateView.as_view(template_name='company-create.html')),
    path('detail/<str:pk>/', TemplateView.as_view(template_name='job-details.html')),
    path('jobs/', TemplateView.as_view(template_name='job-list.html'), name='jobs'),
    path('update/<str:pk>/', TemplateView.as_view(template_name='update-job.html')),
    path('company/', CompanyList.as_view()),
    path('job_list/', JobList.as_view()),
    path('industry/', IndustryList.as_view()),
    path('job_type/', JobTypeList.as_view()),
    path('experience/', ExperienceList.as_view()),
    path('currency/', CurrencyList.as_view()),
    path('qualification/', QualificationList.as_view()),
    path('gender/', GenderList.as_view()),
    path('job_update/<str:pk>/', JobUpdateView.as_view()),
    path('load_job/<str:pk>/', JobObject.as_view()),
    path('load_company/<str:pk>/', CompanyPopulate.as_view()),
    path('job_create/', job_create),
    path('previous_skills/', load_previous_skills),
    path('trending_keyword_save/', trending_keyword_save),
    path('trending_keyword_show/', TrendingKeywordPopulate.as_view()),
    path('popular_categories/', PopularCategories.as_view()),
    path('top_skills/', TopSkills.as_view()),

]