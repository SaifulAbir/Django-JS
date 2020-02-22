from django.urls import path
from django.views.generic import TemplateView
from pro.api import *
urlpatterns = [
    path('profile_create/', TemplateView.as_view(template_name='profile.html')),
    path('create/', profile_create),
    path('register/', TemplateView.as_view(template_name='register.html')),
    path('forget_password/', TemplateView.as_view(template_name='forget_password.html')),
    path('reset_password/', TemplateView.as_view(template_name='reset_password.html')),
    path('terms-and-condition/', TemplateView.as_view(template_name='terms-and-condition.html')),
]