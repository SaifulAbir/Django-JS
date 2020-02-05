from django.urls import path
from django.views.generic import TemplateView
from job.api import *
urlpatterns = [
    path('company', CompanyList.as_view()),
    path('', TemplateView.as_view(template_name='post-job.html')),
    path('details', TemplateView.as_view(template_name='job-details.html')),

]