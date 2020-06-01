from django.urls import path,include

from pro.api_dashboard import skill_job_chart
from pro.api_pro_core import change_password

urlpatterns = [
    path('pro/change-password/', change_password),
    path('skill_job_chart/', skill_job_chart),

]