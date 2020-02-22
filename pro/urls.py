from django.urls import path
from django.views.generic import TemplateView
from pro.api import *
urlpatterns = [
    path('profile-create/', TemplateView.as_view(template_name='profile.html')),
    path('create/', profile_create),
    path('create_with_user/', profile_create_with_user_create),
    path('register/', TemplateView.as_view(template_name='register.html')),
    path('terms-and-condition/', TemplateView.as_view(template_name='terms-and-condition.html')),
]