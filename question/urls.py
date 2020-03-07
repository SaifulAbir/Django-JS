from django.urls import path
from django.views.generic import TemplateView
from .api import *

urlpatterns = [
    path('topic_populate/<int:subject>/', TopicstPopulate.as_view()),
]