from django.urls import path
from django.views.generic import TemplateView
from job.api import *
from job.api_job_list import similar_jobs, applied_jobs, favourite_jobs, recent_jobs, job_list
from job.api_job_related import get_job_site_list, JobSourceList, get_job_nature_list, get_job_type_list, \
    get_job_status_list, get_job_creator_type_list, JobCategoryList, JobGenderList

urlpatterns = [
    path('post-job/', TemplateView.as_view(template_name='post-job.html'), name='post_job'),
    path('validation-test', TemplateView.as_view(template_name='company-create.html')),
    path('job-detail/<slug:slug>/', TemplateView.as_view(template_name='job-details.html')),
    path('jobs/', TemplateView.as_view(template_name='job-list.html'), name='jobs'),
    path('update/<str:pk>/', TemplateView.as_view(template_name='update-job.html')),
    path('company/', CompanyList.as_view()),
    path('company/search/', get_company_by_name),
    path('industry/', IndustryList.as_view()),
    path('job_type/', JobTypeList.as_view()),
    path('experience/', Experience.as_view()),
    path('currency/', CurrencyList.as_view()),
    path('qualification/', QualificationList.as_view()),
    path('gender/', GenderList.as_view()),
    path('job_update/<str:pk>/', JobUpdateView.as_view()),
    path('load_job/<slug:slug>/', JobObject.as_view()),
    path('load_company/<str:pk>/', CompanyPopulate.as_view()),
    path('job_create/', job_create),
    path('favourite_job_add/', favourite_job_add),
    path('previous_skills/', load_previous_skills),
    path('trending_keyword_save/', trending_keyword_save),
    path('trending_keyword_show/', TrendingKeywordPopulate.as_view()),
    path('popular_categories/', PopularCategories.as_view()),
    path('top_skills/', TopSkills.as_view()),
    path('vital_stats/', vital_stats),
    path('popular_jobs/', PopularJobs.as_view()),
    path('salary_range/', salary_range),
    path('skill_list/', SkillList.as_view()),
    path('apply_online_job_add/', apply_online_job_add),
    path('favourite-jobs-delete/<str:identifier>/', del_fav_jobs),

    path('api/job_list/', job_list),
    path('api/recent_jobs/', recent_jobs),
    path('api/applied_jobs/', applied_jobs),
    path('api/favourite-jobs/',favourite_jobs),
    path('api/similar_jobs/<str:identifier>/', similar_jobs),
    path('api/job-source/list/', JobSourceList.as_view()),
    path('api/job-category/list/', JobCategoryList.as_view()),
    path('api/job-gender/list/', JobGenderList.as_view()),
    path('api/job-site/list', get_job_site_list),
    path('api/job-nature/list', get_job_nature_list),
    path('api/job-type/list', get_job_type_list),
    path('api/job-status/list', get_job_status_list),
    path('api/job-creator-type/list', get_job_creator_type_list),

]