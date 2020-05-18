from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('post-job/', TemplateView.as_view(template_name='post-job.html'), name='post_job'),
    path('validation-test', TemplateView.as_view(template_name='company-create.html')),
    path('job-detail/<slug:slug>/', TemplateView.as_view(template_name='job-details.html')),
    path('jobs/', TemplateView.as_view(template_name='job-list.html'), name='jobs'),
    path('update/<str:pk>/', TemplateView.as_view(template_name='update-job.html')),
]