from django.urls import path,include

from pro.api_dashboard import skill_job_chart
from .api_pro_core import change_password
from pro.api import *
from pro.api_dashboard import *
from pro.api_pro_details import *
from pro.api_pro_related import *
from pro.api_pro_core import *

urlpatterns = [
    path('signup-email-verification/<str:token>', professional_signup_email_verification, name='code-verify'),
    path('pro/change-password/', change_password),
    path('skill_job_chart/', skill_job_chart),
    path('pro/create/', profile_create),
    path('pro/create-with-user/', profile_create_with_user_create),
    path('pro/login/', login),
    path('pro/sign-out/', logout),
    path('pro/password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('pro/profile/<str:pk>/', ProfessionalDetail.as_view()),
    path('pro/profile-update/<str:pk>/', ProfessionalUpdateView.as_view()),
    path('pro/job-alert/', job_alert),
    path('pro/job-alert-notification/', job_alert_notification),
    path('pro/profile-update-partial/<str:pk>/', ProfessionalUpdatePartial.as_view()),
    path('pro/static-urls/', StaticUrl),
    path('pro/education-save/', professional_education_save),
    path('pro/education/delete/<str:pk>/', EducationUpdateDelete.as_view()),
    path('pro/skill/save/', professional_skill_save, name = 'professional-skill'),
    path('pro-skill/delete/<str:pk>/', SkillUpdateDelete.as_view()),
    path('pro/work-experience/save/', professional_workexperience_save),
    path('pro/work-experience/delete/<str:pk>/', WorkExperienceUpdateDelete.as_view()),
    path('pro/portfolio/save/', professional_portfolio_save),
    path('pro/portfolio/delete/<str:pk>/', PortfolioUpdateDelete.as_view()),
    path('pro/membership/save/', professional_membership_save),
    path('pro/membership/delete<str:pk>/', MembershipUpdateDelete.as_view()),
    path('pro/certification/save/', professional_certification_save),
    path('pro/certification/update/<str:pk>/', CertificationUpdateDelete.as_view()),
    path('pro/reference/save/', professional_reference_save),
    path('pro/reference/update/<str:pk>/', ReferenceUpdateDelete.as_view()),
    path('pro/education_object/<str:pk>/', EducationObject.as_view()),
    path('pro/recent_activity/', pro_recent_activity),
    path('pro/info_box/', info_box_api),
    path('pro/skill_object/<str:pk>/', SkillObject.as_view()),

    path('religion/', ReligionList.as_view()),
    path('nationality/', NationalityList.as_view()),
    path('organization/', OrganizationList.as_view()),
    path('major/', MajorList.as_view()),
    path('institute/', InstituteList.as_view()),
    path('institute_search/', institute_search),
    path('certificate_name/', CertificateNameList.as_view()),



]