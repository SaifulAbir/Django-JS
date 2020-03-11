from django.db import models
from datetime import datetime

from examinees.models import Examinee
from exams.models import Exam
from questionnaire.models import Questionnaire
from registration.models import Registration
from question.models import Question

class Exampaper(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=True, related_name='exam')
    examinee = models.ForeignKey(Examinee, on_delete=models.CASCADE, blank=True, related_name='examinee')
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, blank=True, related_name='registration')
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, default="")
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
    questionnaire_id = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='questionnaire')
    examinee_id = models.ForeignKey(Examinee, on_delete=models.CASCADE)

    def __str__(self):
        return self.questionnaire_id.name

    class Meta:
        verbose_name_plural = "Assign Questionnaire"
