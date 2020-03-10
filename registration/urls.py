from django.urls import path
from registration.api import *

urlpatterns = [
    path('exam-enroll/', exam_enroll),

]
