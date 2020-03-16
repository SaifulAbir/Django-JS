from django.contrib import admin
from django.shortcuts import render

from .models import Subject, Topics, SubTopics, Difficulty, QuestionType, Question, Answer
from django.utils.html import format_html
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
# Create your views here.
from question.models import *
from resources.strings import YES_TEXT
from resources.strings_question import *
from django.forms.models import BaseInlineFormSet
from django import forms
from resources import strings_question
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

# Register your models here.

class SubjectAdmin(admin.ModelAdmin):
    model = Subject

    list_display = ['name', 'created_date', ]
    search_fields = ['name']
    save_as = True

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

    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
              "js/sub_topic_script.js","js/common.js",)


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
    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
              "js/question_script.js","js/common.js",)

    list_display =['question_id','question_text','qtype','difficulties','subject','topic','sub_topic','status']
    list_per_page = 15
    search_fields =['question_id__iexact','question__icontains','qtype__name__iexact','difficulties__name__iexact',
                    'subject__name__iexact','topic__name__iexact','sub_topic__name__iexact']
    list_filter = (('question',DropdownFilter),('qtype',RelatedDropdownFilter),('status',DropdownFilter),
                   ('difficulties',RelatedDropdownFilter),('subject',RelatedDropdownFilter),
                   ('topic',RelatedDropdownFilter),('sub_topic',RelatedDropdownFilter))
    fields = ['question',('question_id','qtype','difficulties'),('subject','topic','sub_topic', 'status')]
    inlines = [AnswerInline]
    save_as = True

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('detail_view/<int:pk>/', self.detail_view,name= 'ques_detail'),
            path('import/', self.question_import, name='import'),
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

    def generate_result_csv(self, df:pd.DataFrame, row_results, row_msgs):
        df['result'] = row_results
        df['msg'] = row_msgs
        return df.to_csv()

    def question_import(self, request):
        msg = ''
        row_msgs = []
        row_results = []
        if request.method == 'POST' and request.FILES['excelfile']:

            myfile = request.FILES['excelfile']
            file_type = request.FILES['excelfile'].content_type
            file_type = str(file_type)

            # if file_type != EXCEL_CONTENT_TYPE_XLSX or file_type != EXCEL_CONTENT_TYPE_XLX:
            #     return render(request, 'question/excelimport.html', {
            #         'msg': INVALID_EXCEL_FILE_FORMAT_MSG
            #     })

            exceldata = pd.read_excel(myfile)
            excel_column_list = list(exceldata.columns)
            standard_column_name_with_serial = ['Subject', 'Topic', 'Subtopic', 'Difficulties', 'Type', 'Status',
                                                'Question', 'Option One', 'Option One Correct', 'Option Two',
                                                'Option Two Correct', 'Option Three', 'Option Three Correct',
                                                'Option Four', 'Option Four Correct', 'Option Five',
                                                'Option Five Correct']

            if standard_column_name_with_serial != excel_column_list:
                return render(request, 'question/excelimport.html', {
                    'msg': QUESTION_IMPORT_INVALID_COLUMN_ERROR_MSG
                })
            elif exceldata.empty:
                return render(request, 'question/excelimport.html', {
                    'msg': EMPTY_EXCEL_FILE_FORMAT_MSG
                })

            for i in exceldata.index:

                ## Get the subject ID
                try:
                    subject_name = exceldata[EXCEL_COLUMN_SUBJECT][i]
                    subject = Subject.objects.get(name=subject_name)
                except Exception as ex:
                    row_results.append("ERROR")
                    row_msgs.append('This subject ' + exceldata[EXCEL_COLUMN_SUBJECT][i] + ' not found' + str(ex))
                    continue

                ## Get the subject ID
                try:
                    topic_name = exceldata[EXCEL_COLUMN_TOPIC][i]
                    topic = Topics.objects.get(name=topic_name)
                except Topics.DoesNotExist:
                    row_results.append("ERROR")
                    row_msgs.append('This topic ' + exceldata[EXCEL_COLUMN_TOPIC][i] + ' not found')
                    continue

                ## Get the Subtopic ID
                try:
                    subtopic_name = exceldata[EXCEL_COLUMN_SUBTOPIC][i]
                    sub_topic = SubTopics.objects.get(name=subtopic_name)
                except SubTopics.DoesNotExist:
                    row_results.append("ERROR")
                    row_msgs.append('This subtopic ' + exceldata[EXCEL_COLUMN_SUBTOPIC][i] + ' not found')
                    continue

                ## Get the difficulties ID
                try:
                    difficulties = exceldata[EXCEL_COLUMN_DIFFICULTIES][i]
                    difficulties = Difficulty.objects.get(name=difficulties)
                except Difficulty.DoesNotExist:
                    row_results.append("ERROR")
                    row_msgs.append('This difficulty' + exceldata[EXCEL_COLUMN_DIFFICULTIES][i] + ' not found')
                    continue

                ## Get the qtype ID
                try:
                    type = exceldata[EXCEL_COLUMN_QTYPE][i]
                    qtype = QuestionType.objects.get(name=type)
                except QuestionType.DoesNotExist:
                    row_results.append("ERROR")
                    row_msgs.append('This type' + exceldata[EXCEL_COLUMN_QTYPE][i] + ' not found')
                    continue

                # Insert Question && Transaction start from here
                question_text = exceldata[EXCEL_COLUMN_QUESTION][i]

                option_one = exceldata[EXCEL_COLUMN_OPTION_ONE][i]
                option_one_correct = exceldata[EXCEL_COLUMN_OPTION_ONE_CORRECT][i]

                option_two = exceldata[EXCEL_COLUMN_OPTION_TWO][i]
                option_two_correct = exceldata[EXCEL_COLUMN_OPTION_TWO_CORRECT][i]

                option_three = exceldata[EXCEL_COLUMN_OPTION_THREE][i]
                option_three_correct = exceldata[EXCEL_COLUMN_OPTION_THREE_CORRECT][i]

                option_four = exceldata[EXCEL_COLUMN_OPTION_FOUR][i]
                option_four_correct = exceldata[EXCEL_COLUMN_OPTION_FOUR_CORRECT][i]

                question_obj = Question.objects.create(question=question_text, subject=subject, topic=topic,
                                                       sub_topic=sub_topic, qtype=qtype,
                                                       difficulties=difficulties, status=QUESTION_STATUS_PUBLISHED)

                if option_one:
                    if option_one_correct == YES_TEXT:
                        option_one_correct = True
                    else:
                        option_one_correct = False
                    Answer.objects.create(name=option_two, correct=option_one_correct, question=question_obj)

                if option_two:
                    if option_two_correct == YES_TEXT:
                        option_two_correct = True
                    else:
                        option_two_correct = False
                    Answer.objects.create(name=option_one, correct=option_two_correct, question=question_obj)

                if option_three:
                    if option_three_correct == YES_TEXT:
                        option_three_correct = True
                    else:
                        option_three_correct = False
                    Answer.objects.create(name=option_three, correct=option_three_correct, question=question_obj)

                if option_four:
                    if option_four_correct == YES_TEXT:
                        option_four_correct = True
                    else:
                        option_four_correct = False
                    Answer.objects.create(name=option_four, correct=option_four_correct, question=question_obj)

                if exceldata[EXCEL_COLUMN_OPTION_FIVE][i]:
                    option_five = exceldata[EXCEL_COLUMN_OPTION_FIVE][i]
                    option_five_correct = exceldata[EXCEL_COLUMN_OPTION_FIVE_CORRECT][i]
                    if option_five_correct == YES_TEXT:
                        option_five_correct = True
                    else:
                        option_five_correct = False
                    Answer.objects.create(name=option_five, correct=option_five_correct, question=question_obj)
                ## Transaction End here
                row_results.append("OK")
                row_msgs.append("")

            output_file = self.generate_result_csv(exceldata, row_results, row_msgs)
            # df: pd.DataFrame
            # df['result'] = row_results
            # df['msg'] = row_msgs
            # return df.to_csv()

            response = HttpResponse(output_file, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="result.xls"'
            return response
        return render(request, 'admin/excelimport.html', {
            'msg': msg
        })


    # def button(self, obj):
    #
    #     return format_html(
    #         '<a class="button" href="{}">Details</a>',
    #         reverse('admin:ques_detail', args=[obj.pk])
    #     )
    # button.short_description = 'Action'



#Models Register Section

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Topics, TopicsAdmin)
admin.site.register(SubTopics, SubtopicsAdmin)
admin.site.register(Difficulty)
admin.site.register(QuestionType)
admin.site.register(Question,QuestionAdmin)