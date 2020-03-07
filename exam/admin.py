from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from exam.models import Exam, ExamCategory, ExamLevel

class ExamAdmin(ModelAdmin):

    list_display = ['exam_code','exam_name','pass_mark','duration','exam_category','exam_level','subject','topic','sub_topic']

admin.site.register(Exam, ExamAdmin)
admin.site.register(ExamCategory)
admin.site.register(ExamLevel)
