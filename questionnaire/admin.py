import json

from django.contrib import admin
import time
# Register your models here.
from django.core.paginator import Paginator
from django.forms import BaseInlineFormSet, forms
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html

from question.models import Subject, Question, Topics, SubTopics
from resources import strings_questionnaire
from questionnaire.models import Questionnaire, QuestionnaireDetail
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

class QuestionnaireDetailAdmin(admin.ModelAdmin):
    list_display = ['questionnaire_id','question_id']

class QuestionnaireDetailInlineFormset(BaseInlineFormSet):
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
            raise forms.ValidationError(strings_questionnaire.MINIMUM_QUESTION_VALIDATION)

class QuestionnaireDetailInline(admin.StackedInline):
    model = QuestionnaireDetail
    formset = QuestionnaireDetailInlineFormset
    extra = 5

class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['name','subject','topic','sub_topic','remarks','button','button1']
    list_filter = (('name',DropdownFilter),('subject',RelatedDropdownFilter),('topic',RelatedDropdownFilter),
                   ('sub_topic',RelatedDropdownFilter))
    inlines = [QuestionnaireDetailInline]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('questionnaire_creation/', self.questionnaire_create,  name = 'create'),
            path('search_question/', self.search_questions,  name = 'search'),
            path('load_topics/', self.load_topics),
            path('load_sub_topics/', self.load_sub_topics),
            path('questionnaire_detail_view/<int:pk>/', self.questionnaire_detail_view, name='questionnaire_detail'),
            path('questionnaire_update_view/<int:pk>/', self.questionnaire_update_view, name='questionnaire_update_view'),
            path('questionnaire_update/', self.questionnaire_update, name='questionnaire_update'),

        ]
        return my_urls + urls

    def questionnaire_create(self,request):
        sub=Subject.objects.all()
        questionnaire_name = request.POST.get('questionnaire_name')
        subject = request.POST.get('subject')
        topics = request.POST.get('topics')
        sub_topics = request.POST.get('sub_topics')
        remarks = request.POST.get('remarks')

        if questionnaire_name != '' and questionnaire_name is not None:
            quesModel= Questionnaire()
            quesModel.name= questionnaire_name
            quesModel.remarks = remarks
            quesModel.subject_id= subject
            quesModel.topic_id= topics
            quesModel.sub_topic_id= sub_topics
            quesModel.save()


            ques_srting = request.POST.get('ques_id_list')
            ques_list = list(ques_srting.split(","))
            for ques in ques_list[1:]:
                print(ques)
                detailModel = QuestionnaireDetail()
                detailModel.questionnaire_id_id = quesModel.id
                detailModel.question_id_id = ques
                detailModel.save()

        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            sub=sub
        )
        return render(request, "admin/questionnaire_create.html",context)



    def search_questions(self,request):
        data = dict()
        qs = Question.objects.all()
        ques = request.GET.get('question_contains')
        qtype = request.GET.get('qtype_contains')
        difficulty = request.GET.get('difficulty_contains')
        subject = request.GET.get('subject_contains')
        topic = request.GET.get('topic_contains')
        sub_topic = request.GET.get('subtopic_contains')
        if ques != '' and ques is not None:
            qs = qs.filter(question__icontains=ques)
        if qtype != '' and qtype is not None:
            qs = qs.filter(qtype__name__icontains=qtype)
        if difficulty != '' and difficulty is not None:
            qs = qs.filter(difficulties__name__icontains=difficulty)
        if subject != '' and subject is not None:
            qs = qs.filter(subject__name__icontains=subject)
        if topic != '' and topic is not None:
            qs = qs.filter(topic__name__icontains=topic)
        if sub_topic != '' and sub_topic is not None:
            qs = qs.filter(sub_topic__name__icontains=sub_topic)

        paginator = Paginator(qs, 50)
        page = request.GET.get('page')
        ques_list = paginator.get_page(page)
        data['question_list'] = render_to_string('admin/search_result.html',
            {'ques_list':ques_list}
        )
        return JsonResponse(data)

    def load_topics(self,request):
        subject_id = request.GET.get('subject')
        topics= Topics.objects.filter(subject_id = subject_id).order_by('name')
        return render(request,'admin/topic_dropdown_list_options.html', {'topics': topics})

    def load_sub_topics(self, request):
        topic_id = request.GET.get('topic')
        sub_topics = SubTopics.objects.filter(topics=topic_id).order_by('name')
        return render(request, 'admin/sub_topic_dropdown_list_options.html', {'sub_topics': sub_topics})



    def questionnaire_detail_view(self, request,pk):
        # ...
        detail = Questionnaire.objects.get(pk=pk)
        questionnaire_details = QuestionnaireDetail.objects.filter(questionnaire_id=pk)

        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            detail=detail,questionnaire_details=questionnaire_details
        )

        return TemplateResponse(request, "admin/questionnaire_detail_view.html", context)

    def questionnaire_update_view(self,request,pk):
        try:
            ques_name = Questionnaire.objects.get(pk=pk)
        except Questionnaire.DoesNotExist:
            ques_name = None

        questionnaire_details= QuestionnaireDetail.objects.filter(questionnaire_id=pk)
        sub = Subject.objects.all()
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            ques_name = ques_name,questionnaire_details=questionnaire_details,sub=sub,pk=pk

        )

        return render(request, "admin/questionnaire_update.html", context)


    def questionnaire_update(self,request):

        questionnaire_name = request.POST.get('questionnaire_name')
        remarks = request.POST.get('remarks')
        questionnaire_id = request.POST.get('questionnaire_id')
        subject = request.POST.get('subject')
        topics = request.POST.get('topics')
        sub_topics = request.POST.get('sub_topics')

        if questionnaire_name != '' and questionnaire_name is not None:
            quesModel=Questionnaire.objects.get(pk=questionnaire_id)
            quesModel.name = questionnaire_name
            quesModel.remarks = remarks
            quesModel.subject_id = subject
            quesModel.topic_id = topics
            quesModel.sub_topic_id = sub_topics
            quesModel.save()
            ques_srting = request.POST.get('ques_id_list')
            response = {'status': 1,'message': ('Success'), 'url': '/admin/questionnaire/questionnaire/'}
            if ques_srting != '' and ques_srting is not None:
                ques_list = list(ques_srting.split(","))
                QuestionnaireDetail.objects.filter(questionnaire_id=questionnaire_id).delete()
                for ques in ques_list:
                    print(ques)
                    detailModel = QuestionnaireDetail()
                    detailModel.questionnaire_id_id = quesModel.id
                    detailModel.question_id_id = ques
                    detailModel.save()
        else :
            response = {'status': 0, 'message': ("Name Can Not Be Empty")}

        time.sleep(1)

        return HttpResponse(json.dumps(response), content_type='application/json')




    def button(self, obj):

        return format_html(
            '<a class="button" href="{}">Details</a>&nbsp;',
            reverse('admin:questionnaire_detail', args=[obj.pk]),
        )
    button.short_description = 'Action'

    def button1(self, obj):
        return format_html(
            '<a class="button" href="{}">Update</a>',
            reverse('admin:questionnaire_update_view', args=[obj.pk]),
        )
    button1.short_description = ''

admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(QuestionnaireDetail, QuestionnaireDetailAdmin)
