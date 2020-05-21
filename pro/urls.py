from django.urls import path,include
from django.views.generic import TemplateView
from django_rest_passwordreset import urls
from pro.api import *
from . import api as pro_views
from .api_pro_core import change_password

urlpatterns = [
    path('profile-update/<str:pk>/', TemplateView.as_view(template_name='profile.html')),
    path('myprofile_info/<str:pk>/', TemplateView.as_view(template_name='myprofile.html'), name='myprofile'),
    path('profile-dashboard/', TemplateView.as_view(template_name='dashboard.html')),
    path('create/', profile_create),
    path('create_with_user/', profile_create_with_user_create),
    path('login/', login),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('reset-password-successful/', TemplateView.as_view(template_name='reset-password-successful.html')),
    path('sign-in/', TemplateView.as_view(template_name='sign-in.html')),
    path('sign-out/', logout),
    path('sign-in/', TemplateView.as_view(template_name='sign-in.html'), name='sign-in'),
    # path('sign-up-verification/', TemplateView.as_view(template_name='sign-up-verification.html')),
    path('signup-email-verification/<str:token>', professional_signup_email_verification , name='code-verify'),
    path('forget-password/', TemplateView.as_view(template_name='forget_password.html')),
    path('reset-password-email/', TemplateView.as_view(template_name='reset_email_successful.html')),
    path('password-reset/<str:token>/', TemplateView.as_view(template_name='reset_password.html')),
    path('terms-and-condition/', TemplateView.as_view(template_name='terms-and-condition.html')),
    # path('reset-password/verify-token/', pro_views.CustomPasswordTokenVerificationView.as_view(), name='password_reset_verify_token'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('profile/<str:pk>/', ProfessionalDetail.as_view()),
    path('profile_update/<str:pk>/', ProfessionalUpdateView.as_view()),
    path('job_alert/', job_alert),
    path('job_alert_notification/', job_alert_notification),
    path('profile_update_partial/<str:pk>/', ProfessionalUpdatePartial.as_view()),
    # path('professional_info/<str:pk>/', professional_info),
    path('myprofile/<str:pk>/', TemplateView.as_view(template_name='profiles.html'),name='profile'),
    path('static_urls/', StaticUrl),
    path('professional_education/', professional_education_save),
    path('professional_education/<str:pk>/', EducationUpdateDelete.as_view()),
    path('professional_skill/', professional_skill_save, name = 'professional-skill'),
    path('professional_skill/<str:pk>/', SkillUpdateDelete.as_view()),
    path('professional_work_experience/', professional_workexperience_save),
    path('professional_work_experience/<str:pk>/', WorkExperienceUpdateDelete.as_view()),
    path('professional_portfolio/', professional_portfolio_save),
    path('professional_portfolio/<str:pk>/', PortfolioUpdateDelete.as_view()),
    path('professional_membership/', professional_membership_save),
    path('professional_membership/<str:pk>/', MembershipUpdateDelete.as_view()),
    path('professional_certification/', professional_certification_save),
    path('professional_certification/<str:pk>/', CertificationUpdateDelete.as_view()),
    path('professional_reference/', professional_reference_save),
    path('professional_reference/<str:pk>/', ReferenceUpdateDelete.as_view()),
    path('professional_education_object/<str:pk>/', EducationObject.as_view()),
    path('religion/', ReligionList.as_view()),
    path('nationality/', NationalityList.as_view()),
    path('organization/', OrganizationList.as_view()),
    path('major/', MajorList.as_view()),
    path('institute/', InstituteList.as_view()),
    path('institute_search/', institute_search),
    path('certificate_name/', CertificateNameList.as_view()),
    path('applied-jobs/', TemplateView.as_view(template_name='applied_jobs.html'),name='applied_jobs'),
    path('favourite_jobs/', TemplateView.as_view(template_name='favourite_jobs.html'),name='favourite_jobs'),
    path('professional_skill_object/<str:pk>/', SkillObject.as_view()),


    path('info_box/', info_box_api),
    path('skill_job_chart/', skill_job_chart),
    path('pro_recent_activity/', pro_recent_activity),
    path('change_password/<str:pk>/', TemplateView.as_view(template_name='change_password.html')),

]