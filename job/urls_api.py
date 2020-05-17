from django.urls import path
from django.views.generic import TemplateView

from job.api import IndustryList, JobTypeList, Experience, CurrencyList, QualificationList, GenderList, JobUpdateView, \
    CompanyPopulate, job_create, favourite_job_add, load_previous_skills, trending_keyword_save, \
    TrendingKeywordPopulate, PopularCategories, TopSkills, vital_stats, PopularJobs, salary_range, SkillList, \
    apply_online_job_add, del_fav_jobs
from job.api_company import CompanyList, get_company_by_name
from job.api_job_core import JobObject
from job.api_job_list import similar_jobs, applied_jobs, favourite_jobs, recent_jobs, job_list
from job.api_job_related import get_job_site_list, JobSourceList, get_job_nature_list, get_job_type_list, \
    get_job_status_list, get_job_creator_type_list, JobCategoryList, JobGenderList

urlpatterns = [
    # TODO: review >>>
    path('industry/', IndustryList.as_view()),
    path('job_type/', JobTypeList.as_view()),
    path('experience/', Experience.as_view()),
    path('currency/', CurrencyList.as_view()),
    path('qualification/', QualificationList.as_view()),
    path('gender/', GenderList.as_view()),
    path('job_update/<str:pk>/', JobUpdateView.as_view()),
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
    # <<<

    path('job/search/', job_list),
    path('job/recent/', recent_jobs),
    path('job/applied/', applied_jobs),
    path('job/favourite/', favourite_jobs),
    path('job/similar/<str:identifier>/', similar_jobs),
    path('job/get/<slug:slug>/', JobObject.as_view()),
    path('job-source/list/', JobSourceList.as_view()),
    path('job-category/list/', JobCategoryList.as_view()),
    path('job-gender/list/', JobGenderList.as_view()),
    path('job-site/list', get_job_site_list),
    path('job-nature/list', get_job_nature_list),
    path('job-type/list', get_job_type_list),
    path('job-status/list', get_job_status_list),
    path('job-creator-type/list', get_job_creator_type_list),

    path('company/', CompanyList.as_view()),
    path('company/search/', get_company_by_name),
]