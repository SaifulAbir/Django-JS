from django.urls import path,include
from django.views.generic import TemplateView
from django_rest_passwordreset import urls
from pro.api import *
from . import api as pro_views
urlpatterns = [
    path('profile-update/<str:pk>/', TemplateView.as_view(template_name='profile.html')),
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
    path('password-reset/<str:token>/', TemplateView.as_view(template_name='reset_password.html')),
    path('terms-and-condition/', TemplateView.as_view(template_name='terms-and-condition.html')),
    # path('reset-password/verify-token/', pro_views.CustomPasswordTokenVerificationView.as_view(), name='password_reset_verify_token'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('profile/<str:pk>/', ProfessionalDetail.as_view()),
    path('profile_update/<str:pk>/', ProfessionalUpdateView.as_view()),
    path('job_alert/', job_alert),
    path('job_alert_notification/', job_alert_notification),
    path('profile_update_partial/<str:pk>/', ProfessionalUpdatePartial.as_view()),
    path('professional_education_save/', ProfessionalEducationSave.as_view()),
    path('professional_skill_save/', professional_skill_save),
    path('professional_work_experience_save/', professional_workexperience_save),
    path('professional_portfolio_save/', professional_portfolio_save),
    path('professional_membership_save/', professional_membership_save),
    path('professional_certification_save/', professional_certification_save),
    path('professional_reference_save/', professional_reference_save),
    # path('professional_info/<str:pk>/', professional_info),
]