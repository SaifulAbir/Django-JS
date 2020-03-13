from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from exam.models import Exam
from questionnaire.models import Questionnaire
from registration.models import Registration
from question.models import Question

class Exampaper(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=True, related_name='exam')
    professional = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='professional')
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, blank=True, related_name='registration')
    question = models.ForeignKey(Question, on_delete=models.PROTECT, blank=True, default="")
    question_text = models.TextField()
    answers_id = models.CharField(max_length=200)
    submitted_ans_id = models.CharField(max_length=200)
    correct = models.BooleanField(blank=False, default=False)
    created_date = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name_plural = "Exam Paper"
        db_table= 'exam_paper'

class AssignQuestionnaire(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.PROTECT, related_name='questionnaire')
    professional = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.questionnaire.id

    class Meta:
        verbose_name_plural = "Assign Questionnaire"
