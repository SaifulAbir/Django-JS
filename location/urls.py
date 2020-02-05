from django.urls import path
from django.views.generic import TemplateView
from .api import *
urlpatterns = [
    path('division', DivisionListCreate.as_view()),
    path('division/<str:pk>/', DivisionUpdateDestroy.as_view()),
    path('district', District.as_view()),

]