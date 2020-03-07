from django.urls import path
from django.views.generic import TemplateView
from .api import *

urlpatterns = [
    path('topic_populate/<int:subject>/', TopicstPopulate.as_view()),
    path('sub_topic_populate/<int:topic>/', SubTopicstPopulate.as_view()),
]