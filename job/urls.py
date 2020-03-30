from django.urls import path
from django.views.generic import TemplateView
from job.api import *
from .test_api import TrendingKeywordsPopulator,save_trending_keys
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
    # url_for_test_api
    path('show_trending_key/',TrendingKeywordsPopulator.as_view()),
    path('home/', TemplateView.as_view(template_name='home_test.html')),
    path('show_trending_save/',save_trending_keys),

]