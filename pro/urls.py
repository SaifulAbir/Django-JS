from django.urls import path,include
from django.views.generic import TemplateView
from django_rest_passwordreset import urls
from pro.api import *

urlpatterns = [
    path('profile-layout/', TemplateView.as_view(template_name='professional_layout.html')),
    path('myprofile-info/<str:pk>/', TemplateView.as_view(template_name='myprofile.html'), name='myprofile'),
    path('profile-dashboard/', TemplateView.as_view(template_name='dashboard.html')),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('reset-password-successful/', TemplateView.as_view(template_name='reset-password-successful.html')),
    path('sign-in/', TemplateView.as_view(template_name='sign-in.html'), name='sign-in'),
    path('forgot-password/', TemplateView.as_view(template_name='forget_password.html')),
    path('reset-password-confirm/', TemplateView.as_view(template_name='reset_email_successful.html')),
    path('reset-password/<str:token>/', TemplateView.as_view(template_name='reset_password.html')),
    path('terms-and-condition/', TemplateView.as_view(template_name='terms-and-condition.html')),
    path('myprofile/<str:pk>/', TemplateView.as_view(template_name='profiles.html'), name='profile'),
    path('applied-jobs/', TemplateView.as_view(template_name='applied_jobs.html'),name='applied_jobs'),
    path('favourite-jobs/', TemplateView.as_view(template_name='favourite_jobs.html'),name='favourite_jobs'),
    path('change-password/<str:pk>/', TemplateView.as_view(template_name='change_password.html'), name='change_password'),




]