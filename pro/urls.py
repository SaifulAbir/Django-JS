from django.urls import path
from django.views.generic import TemplateView
from pro.api import *
urlpatterns = [
    path('profile-create/', TemplateView.as_view(template_name='profile.html')),
    path('create/', profile_create),
    path('create_with_user/', profile_create_with_user_create),
    path('register/', TemplateView.as_view(template_name='register.html')),
    path('sign-in/', TemplateView.as_view(template_name='sign-in.html')),
    path('sign-up-verification/<str:id>/', TemplateView.as_view(template_name='sign-up-verification.html')),
    path('signup-email-verification/', professional_signup_email_verification , name='code-verify'),
    path('forget-password/', TemplateView.as_view(template_name='forget_password.html')),
    path('reset-password/', TemplateView.as_view(template_name='reset_password.html')),
    path('terms-and-condition/', TemplateView.as_view(template_name='terms-and-condition.html')),
]