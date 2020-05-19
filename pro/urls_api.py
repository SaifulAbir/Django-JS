from django.urls import path,include

from pro.api_pro_core import change_password

urlpatterns = [
    path('pro/change-password/', change_password)
]