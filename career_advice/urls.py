from django.urls import path
from django.views.generic import TemplateView
from .api import *

urlpatterns = [
    path('career_advise_show/', CareerAdviseShow.as_view()),
    path('career_advise/', CareerAdvise.as_view()),
]