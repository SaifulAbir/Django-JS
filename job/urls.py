from django.urls import path
from django.views.generic import TemplateView
urlpatterns = [
    path('foo/', TemplateView.as_view(template_name='job-details.html'))
]