from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin
from django.forms import BaseInlineFormSet, forms

from exam.models import Exam, ExamCategory, ExamLevel, ExamQuestionnaireDetails
from resources import strings_questionnaire


class QuestionnaireDetailFormset(BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if count < 1:
            raise forms.ValidationError(strings_questionnaire.MINIMUM_QUESTIONNAIRE_VALIDATION)

class ExamQuestionnaireInline(admin.StackedInline):
    model = ExamQuestionnaireDetails
    formset = QuestionnaireDetailFormset
    extra = 3

class ExamAdmin(ModelAdmin):
    list_display = ['exam_code','exam_name','pass_mark','duration','exam_category','exam_level','subject','topic','sub_topic']
    inlines = [ExamQuestionnaireInline]

admin.site.register(Exam, ExamAdmin)
admin.site.register(ExamCategory)
admin.site.register(ExamLevel)
