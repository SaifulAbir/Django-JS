from django.urls import path

from .views import *

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('result/<int:registration_id>', result),
    path('submit', exam_submit),
    path('index', index),
    path('result-list', ResultListView.as_view(), name='result-list')
]