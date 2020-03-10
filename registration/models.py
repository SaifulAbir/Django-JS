from django.db import models
from exam.models import Exam
from resources.strings import *
from django.contrib.auth.models import User

CHOICES = (
        ('1', 'Failed'),
        ('2', 'Pending'),
        ('3', 'Passed'),
    )
# Create your models here.
class Registration(models.Model):
    professional = models.ForeignKey(User, on_delete=models.CASCADE, related_name='professional_exam_registration', blank=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_registration', blank=True)
    result_status = models.CharField(max_length=100, choices=CHOICES, default=2)
    percentage_of_correct = models.IntegerField(default=0)
    status = models.CharField(max_length=250)
    exam_submitted_date= models.DateTimeField(blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = "registration"
        db_table='registration'