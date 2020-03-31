from django.urls import path
from django.views.generic import TemplateView
from .api import *
from .test_api import CareerAdviceshow

urlpatterns = [
    path('career_advise_show/', CareerAdviseShow.as_view()),
    # TEST_API_TEST
    path('show_career_advice/', CareerAdviceshow.as_view()),
]