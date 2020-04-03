from django.urls import path
from django.views.generic import TemplateView
from .api import *
urlpatterns = [
    path('division', DivisionListCreate.as_view()),
    # path('division/<str:pk>/', DivisionUpdateDestroy.as_view()),
    # path('company_create/', company_create),
    # path('company_update/<int:pk>/', CompanyUpdateView.as_view()),
    path('district_populate/<str:division>/', DistrictPopulate.as_view()),
    # path('district', DistrictList.as_view()),
]