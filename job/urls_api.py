from django.urls import path

from job.api_misc import apply_online, get_vital_stats, save_trending_keywords, \
    toggle_favourite
from job.api_company import get_company_by_name, CompanyList
from job.api_job_core import JobAPI, JobUpdateView, create_job
from job.api_job_kpi import TopFavouriteList, TopCategoryList, TopSkillList, TopCompanyList, TrendingKeywordList
from job.api_job_list import similar_jobs, applied_jobs, favourite_jobs, recent_jobs, job_list
from job.api_job_related import get_job_site_list, JobSourceList, get_job_nature_list, get_job_type_list, \
    get_job_status_list, get_job_creator_type_list, JobCategoryList, JobGenderList, IndustryList, JobTypeList, \
    ExperienceList, CurrencyList, QualificationList, GenderList, SkillList, get_salary_range

urlpatterns = [
    path('job/search/', job_list),
    path('job/recent/', recent_jobs),
    path('job/applied/', applied_jobs),
    path('job/favourite/', favourite_jobs),
    path('job/similar/<str:identifier>/', similar_jobs),
    path('job/get/<slug:slug>/', JobAPI.as_view()),
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

    path('job/apply/', apply_online),
    path('job/favourite/toggle', toggle_favourite),

    path('job/top-favourites/', TopFavouriteList.as_view()),
    path('job/top-categories/', TopCategoryList.as_view()),
    path('job/top-skills/', TopSkillList.as_view()),
    path('job/top-companies/', TopCompanyList.as_view()),
    path('job/trending_keywords/', TrendingKeywordList.as_view()),

    path('skill/list/', SkillList.as_view()),
    path('job/salary-range/', get_salary_range),

    path('job/update/<str:pk>/', JobUpdateView.as_view()),
    path('job/create/', create_job),
    path('job/trending_keywords/save/', save_trending_keywords),
    path('vital_stats/get/', get_vital_stats),

]