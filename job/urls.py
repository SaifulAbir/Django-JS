from django.urls import path
from django.views.generic import TemplateView
from job.api import *
urlpatterns = [
    path('', TemplateView.as_view(template_name='post-job.html')),
    # path('company/', CompanyList.as_view()),
    # path('add', TemplateView.as_view(template_name='company-create.html')),
    # path('list', TemplateView.as_view(template_name='company-list.html')),
    # path('update', TemplateView.as_view(template_name='company-update.html')),
    # path('details', TemplateView.as_view(template_name='job-details.html')),
    # path('job', JobList.as_view()),

]