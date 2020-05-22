from django.urls import path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('company/post-job/', TemplateView.as_view(template_name='post-job.html'), name='post_job'),
    path('validation-test', TemplateView.as_view(template_name='company-create.html')),
    path('job-detail/<slug:slug>/', TemplateView.as_view(template_name='job-details.html')),
    path('jobs/', jobs, name='jobs'),
    path('update/<str:pk>/', TemplateView.as_view(template_name='update-job.html')),
    path('company/sign-in/', TemplateView.as_view(template_name='company_sign_in.html'), name='company_sign'),
    path('company/forgot-password/', TemplateView.as_view(template_name='company_forget_password.html'), name='company_forgot'),
    path('company/reset-password/', TemplateView.as_view(template_name='company_reset_password.html'), name='company_reset'),
    path('company/reset-password-successful/', TemplateView.as_view(template_name='company-reset-password-successful.html'), name='reset_success'),
    path('company/edit-profile/', TemplateView.as_view(template_name='company_edit_profile.html'), name='company_edit'),
]