from django.contrib import admin
from .models import Subject, Topics, SubTopics, Difficulty, QuestionType, Question, Answer
from django.utils.html import format_html
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter
from django.forms.models import BaseInlineFormSet
from django import forms
from resources import strings_question
# Register your models here.

class SubjectAdmin(admin.ModelAdmin):
    model = Subject

    list_display = ['name', 'created_date', ]
    search_fields = ['name']

class TopicsAdmin(admin.ModelAdmin):
    model = Topics
    list_display = ['name','get_subject', 'created_date']
    search_fields = ['name']

    def get_subject(self, obj):
        return obj.subject_id.name

    get_subject.short_description = 'Subject'

class SubtopicsAdmin(admin.ModelAdmin):
    model = SubTopics
    list_display = ['name', 'subject','topics', 'created_date', ]
    search_fields = ['name']


class AnswerInlineFormset(BaseInlineFormSet):
    def clean(self):
        correct_count=0
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
                if form.cleaned_data.get('correct',True):
                    correct_count += 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if count < 2:
            raise forms.ValidationError(strings_question.MINIMUM_ANSWER_VALIDATION)
        if correct_count < 1:
            raise forms.ValidationError(strings_question.MINIMUM_CORRECT_ANSWER_VALIDATION)



class AnswerInline(admin.StackedInline):
    model = Answer
    formset = AnswerInlineFormset
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    # class Media:
    #     js = ("js/question_script.js","js/common.js",)

    list_display =['question_id','question_text','qtype','difficulties','subject','topic','sub_topic','status','button']
    list_per_page = 15
    search_fields =['question_id__iexact','question__icontains','qtype__name__iexact','difficulties__name__iexact',
                    'subject__name__iexact','topic__name__iexact','sub_topic__name__iexact']
    list_filter = (('question',DropdownFilter),('qtype',RelatedDropdownFilter),('status',DropdownFilter),
                   ('difficulties',RelatedDropdownFilter),('subject',RelatedDropdownFilter),
                   ('topic',RelatedDropdownFilter),('sub_topic',RelatedDropdownFilter))
    fields = ['question',('question_id','qtype','difficulties'),('subject','topic','sub_topic', 'status')]
    inlines = [AnswerInline]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('detail_view/<int:pk>/', self.detail_view,name= 'ques_detail'),

        ]
        return my_urls + urls

    def detail_view(self, request,pk):
        # ...
        detail = Question.objects.get(pk=pk)
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            detail=detail
        )

        return TemplateResponse(request, "admin/detail_view.html", context)


    def button(self, obj):

        return format_html(
            '<a class="button" href="{}">Details</a>',
            reverse('admin:ques_detail', args=[obj.pk])
        )
    button.short_description = 'Action'



#Models Register Section

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Topics, TopicsAdmin)
admin.site.register(SubTopics, SubtopicsAdmin)
admin.site.register(Difficulty)
admin.site.register(QuestionType)
admin.site.register(Question,QuestionAdmin)