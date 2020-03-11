from django.urls import path
from django.views.generic import TemplateView
from .api import *

urlpatterns = [
    path('topic_populate/<int:subject>/', topics_populate),
    path('sub_topic_populate/<int:topic>/', sub_topics_populate),
    path('list/', QuestionListWithAns.as_view()),
    path('list/<int:exam_id>', QuestionListWithAnsFromQuestionnaire.as_view()),
]