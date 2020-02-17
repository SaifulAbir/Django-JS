from django.urls import path
from django.views.generic import TemplateView
from pro.api import *
urlpatterns = [
    path('profile_create/', TemplateView.as_view(template_name='profile.html')),
    path('create/', profile_create),
]