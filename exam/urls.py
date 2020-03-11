from django.urls import path
from exam.api import *

urlpatterns = [
    path('exam-instruction/<int:exam_id>', exam_instruction),
    path('enrolled-examlist/<int:user_id>', enrolled_examlist),
    path('featured-examlist/<int:user_id>', featured_examlist),
    path('recent-examlist/<int:user_id>', recent_examlist)
]