from django.urls import path
from django.views.generic import TemplateView
from .api import *
urlpatterns = [
    path('division/', Division.as_view()),
    path('district/', District.as_view()),
]