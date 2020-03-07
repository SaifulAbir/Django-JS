from ckeditor.fields import RichTextField
from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
# from questionnaire.models import Questionnaire
# from questionnaire_template.models import Template
from question.models import Subject, Topics, SubTopics
from resources import strings_exam

tag_choice=(
    ("exam", strings_exam.EXAM_TAG_CHOICE),
    ("questionnaire", strings_exam.QUESTIONNAIRE_TAG_CHOICE),
)

class ExamCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = strings_exam.EXAMCATEGORY_VERBOSE_NAME_SINGLE
        verbose_name_plural = strings_exam.EXAMCATEGORY_VERBOSE_NAME_PLURAL
        db_table='exams_category'

class ExamLevel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = strings_exam.EXAMLEVEL_VERBOSE_NAME_SINGLE
        verbose_name_plural = strings_exam.EXAMLEVEL_VERBOSE_NAME_PLURAL
        db_table='exams_level'

class Exam(models.Model):
    exam_code = models.CharField(max_length=50)
    exam_name = models.CharField(max_length=256)
    pass_mark = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    exam_category = models.ForeignKey(ExamCategory, on_delete=models.CASCADE, blank=True, null=True)
    exam_level = models.ForeignKey(ExamLevel, on_delete=models.CASCADE, blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, null=True, blank=True)
    sub_topic = models.ForeignKey(SubTopics, on_delete=models.CASCADE, null=True, blank=True)
    is_featured = models.BooleanField(default=False, blank=True, null=True)
    instruction = RichTextField()
    question_selection_type = models.CharField(max_length=30, null=True, blank=True)
    # template = models.ForeignKey(Template,null=True,blank=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    exam_type = models.CharField(max_length=50, null=True, blank=True)
    exam_fee = models.CharField(max_length=100, null=True, blank=True)
    promo_code = models.CharField(max_length=256, null=True, blank=True)
    discount_price= models.CharField(max_length=128, null=True, blank=True)
    discount_percent = models.CharField(max_length=128, null=True, blank=True)
    re_registration_delay = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return self.exam_name

    class Meta:
        verbose_name = strings_exam.EXAM_VERBOSE_NAME_SINGLE
        verbose_name_plural = strings_exam.EXAM_VERBOSE_NAME_PLURAL
        db_table='exams'

class Tag(models.Model):
    tag_name = models.CharField(max_length=256, blank=True, null=True)
    tag_type = models.CharField(max_length=50, choices=tag_choice)
    tags = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = strings_exam.TAG_VERBOSE_NAME_SINGLE
        verbose_name_plural = strings_exam.TAG_VERBOSE_NAME_PLURAL
        db_table='tags'

# class ExamQuestionnaireDetails(models.Model):
#     exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
#     questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table= 'exam_questionnaire_details'

