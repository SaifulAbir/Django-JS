from django.urls import path

from job.api import SkillList, apply_online_job_add, salary_range, vital_stats, trending_keyword_save, \
    load_previous_skills, favourite_job_add, job_create, JobUpdateView
from job.api_company import get_company_by_name, CompanyList
from job.api_job_core import JobObject
from job.api_job_kpi import TopFavouriteList, TopCategoryList, TopSkillList, TopCompanyList, TrendingKeywordList
from job.api_job_list import similar_jobs, applied_jobs, favourite_jobs, recent_jobs, job_list
from job.api_job_related import get_job_site_list, JobSourceList, get_job_nature_list, get_job_type_list, \
    get_job_status_list, get_job_creator_type_list, JobCategoryList, JobGenderList, IndustryList, JobTypeList, \
    ExperienceList, CurrencyList, QualificationList, GenderList

urlpatterns = [
    # TODO: review >>>

    path('job_update/<str:pk>/', JobUpdateView.as_view()),
    path('job_create/', job_create),
    path('previous_skills/', load_previous_skills),
    path('trending_keyword_save/', trending_keyword_save),

    path('vital_stats/', vital_stats),
    path('salary_range/', salary_range),
    path('skill_list/', SkillList.as_view()),
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

    path('company/list', CompanyList.as_view()),
    path('company/search/', get_company_by_name),

    path('industry/list', IndustryList.as_view()),
    path('job_type/list', JobTypeList.as_view()),
    path('experience/list', ExperienceList.as_view()),
    path('currency/list', CurrencyList.as_view()),
    path('qualification/list', QualificationList.as_view()),
    path('gender/list', GenderList.as_view()),

    path('job/apply/', apply_online_job_add),
    path('job/favourite/toggle', favourite_job_add),

    path('job/top-favourites/', TopFavouriteList.as_view()),
    path('job/top-categories/', TopCategoryList.as_view()),
    path('job/top-skills/', TopSkillList.as_view()),
    path('job/top-companies/', TopCompanyList.as_view()),
    path('job/trending_keywords/', TrendingKeywordList.as_view()),

]