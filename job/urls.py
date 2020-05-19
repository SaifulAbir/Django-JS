from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('post-job/', TemplateView.as_view(template_name='post-job.html'), name='post_job'),
    path('validation-test', TemplateView.as_view(template_name='company-create.html')),
    path('job-detail/<slug:slug>/', TemplateView.as_view(template_name='job-details.html')),
    path('jobs/', TemplateView.as_view(template_name='job-list.html'), name='jobs'),
    path('sign-in/', TemplateView.as_view(template_name='company_sign_in.html'), name='company_sign'),
    path('company-forgot/', TemplateView.as_view(template_name='company_forget_password.html'), name='company_forgot'),
    path('company-reset/', TemplateView.as_view(template_name='company_reset_password.html'), name='company_reset'),
    path('company-reset-success/', TemplateView.as_view(template_name='company-reset-password-successful.html'), name='reset_success'),
    path('company-edit/', TemplateView.as_view(template_name='company_edit_profile.html'), name='company_edit'),
]