from django.contrib import admin, messages

# Register your models here.
from django.contrib.admin import ModelAdmin
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html

# from questionnaire_template.models import Template
# from exams.forms import ExamForm
# from exams.models import Exam, ExamCategory, ExamLevel, Tag, tag_choice, ExamQuestionnaireDetails
# from questionnaire.models import Questionnaire
# from sub_topics.models import SubTopics
# from subject.models import Subject
# from topics.models import Topics
from exam.forms import ExamForm
from exam.models import ExamLevel, ExamCategory, ExamQuestionnaireDetails, Exam, Tag
from question.models import Subject, Topics, SubTopics
from questionnaire.models import Questionnaire
from resources import strings_exam as exam_strings
from resources.strings_exam import *


class ExamAdmin(ModelAdmin):

    list_display = ['exam_name','exam_code','pass_mark','duration','exam_category','exam_level','subject','topic','sub_topic','button']
    list_display_links = ('exam_name',)
    class Media:
        js = (
            'js/exam.js',
        )
        # css={'all': ('assets/css/bootsrap.min.css')}
        css = {
            'all': ('assets/css/bootstrap.min.css',)
        }

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('exam_create/', self.exam_create, name='exam_create'),
            path('load_topics/', self.load_topics, name='load_topics'),
            path('load_sub_topics/', self.load_sub_topics, name='load_sub_topics'),
            path('load_previous_tags/', self.load_previous_tags, name='load_previous_tags'),
            path('search_questionnaire/', self.search_questionnaire, name='search_questionnaire'),
            path('exam_detail_view/<int:pk>/', self.exam_detail_view, name='exam_template_detail'),

        ]
        return my_urls + urls

    def exam_create(self, request):
        questionnaire_list = Questionnaire.objects.all()
        subject_list = Subject.objects.all()
        # template_list = Template.objects.all()
        exam_category_list = ExamCategory.objects.all()
        exam_level_list = ExamLevel.objects.all()
        if request.method == 'POST':
            exam_form = ExamForm(request.POST)

            if exam_form.is_valid():
                exam_code = request.POST.get('exam_code')
                exam_name = request.POST.get('exam_name')
                exam_tags = request.POST.get('tags')
                pass_mark = request.POST.get('pass_mark')
                duration = request.POST.get('duration')
                image = request.FILES.get('image')
                exam_category = request.POST.get('exam_category')
                exam_level = request.POST.get('exam_level')
                subject = request.POST.get('subject')
                topic = request.POST.get('topic')
                sub_topic = request.POST.get('sub_topic')
                is_featured = request.POST.get('is_featured') == 'on'
                instruction = request.POST.get('instruction')
                exam_fee = request.POST.get('exam_fee')
                re_registration_delay = request.POST.get('re_registration_delay')
                question_selection_type = request.POST.get('question_selection_type')
                exam_type = request.POST.get('exam_type')
                promo_code = request.POST.get('promo_code')
                discount_price = request.POST.get('discount_price')
                discount_percent = request.POST.get('discount_percent')
                exam = Exam(exam_code=exam_code, exam_name=exam_name, pass_mark=pass_mark, duration=duration, image=image, subject_id=subject, topic_id=topic,
                            sub_topic_id=sub_topic,exam_fee=exam_fee,re_registration_delay=re_registration_delay, exam_category_id=exam_category, exam_level_id=exam_level, is_featured=is_featured, instruction=instruction,
                            question_selection_type=question_selection_type, promo_code=promo_code,discount_price=discount_price,
                            discount_percent=discount_percent,exam_type=exam_type)

                if question_selection_type == MANUAL:
                    questionnaire = request.POST.getlist('questionaire_id_list[]')
                    if len(questionnaire) >= 1 :
                        exam.save()
                        for ques in questionnaire:
                            questionnaireModel = ExamQuestionnaireDetails()
                            questionnaireModel.exam_id = exam.id

                            print(ques)
                            questionnaireModel.questionnaire_id = ques
                            questionnaireModel.save()
                        messages.success(request, EXAM_SAVE_SUCCESSFULLY_MSG)
                        return HttpResponseRedirect('/admin/exam/exam/')
                    else:
                        messages.error(request, MINIUM_ONE_QUESTIONNAIRE_MUST_BE_SELECTED_MSG)
                        return HttpResponseRedirect('/admin/exam/exam/exam_create/')

                if question_selection_type == AUTO:
                    questionnaire = request.POST.get('template')
                    if questionnaire != '':
                        exam.template_id = questionnaire
                        exam.save()
                        messages.success(request,EXAM_SAVE_SUCCESSFULLY_MSG)
                        return HttpResponseRedirect('/admin/exam/exam/')
                    else:
                        messages.error(request, TEMPLATE_MUST_BE_SELECTED_MSG)
                        return HttpResponseRedirect('/admin/exam/exam/exam_create/')


                if exam_tags:
                    exam_tag_list = exam_tags.split(',')
                    for exam_tag in exam_tag_list:
                        tag = Tag(tag_name=exam_tag, tag_type='exam', tags = exam.id)
                        tag.save()

        else:
            exam_form = ExamForm()
            #exam_form = ExamForm({'question_selection_type': 'auto'})

        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            subject_list = subject_list,
            exam_category_list = exam_category_list,
            exam_level_list = exam_level_list,
            exam_form = exam_form,
            questionnaire_list = questionnaire_list,
            # template_list =template_list,
            exam_strings = exam_strings
        )
        return TemplateResponse(request, "admin/exam_create.html", context)

    def exam_detail_view(self,request,pk):
        detail = Exam.objects.get(pk=pk)
        template_details = ExamQuestionnaireDetails.objects.filter(exam=pk)
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            detail=detail, questionnaire_details=template_details, exam_strings = exam_strings
        )

        return TemplateResponse(request, "admin/exam_detail_view.html", context)

    def button(self, obj):
        return format_html(
            '<a class="button" href="{}">Details</a>&nbsp;',
            reverse('admin:exam_template_detail', args=[obj.pk]),
            )

    button.short_description = ACTIOIN_BUTTON

    def search_questionnaire(self, request):
        data = dict()
        questionnaire_list = Questionnaire.objects.all()
        if request.method=='POST':
            questionnaire_name = request.POST.get('questionnaire-name')
            questionnaire_subject = request.POST.get('questionnaire-subject')
            questionnaire_topic = request.POST.get('questionnaire-topic')
            questionnaire_sub_topic = request.POST.get('questionnaire-sub-topic')
            if questionnaire_name != '' and questionnaire_name is not None:
                questionnaire_list = questionnaire_list.filter(name__icontains=questionnaire_name)
            if questionnaire_subject != '' and questionnaire_subject is not None:
                questionnaire_list = questionnaire_list.filter(subject__name__icontains=questionnaire_subject)
            if questionnaire_topic != '' and questionnaire_topic is not None:
                questionnaire_list = questionnaire_list.filter(topic__name__icontains=questionnaire_topic)
            if questionnaire_sub_topic != '' and questionnaire_sub_topic is not None:
                questionnaire_list = questionnaire_list.filter(sub_topic__name__icontains=questionnaire_sub_topic)
            data['questionnaire_list'] = render_to_string('admin/exam/questionnaire_list.html', {'questionnaire_list': questionnaire_list}, request=request)
            return JsonResponse(data)
        data['form'] = render_to_string('admin/exam/search_questionnaire_form.html', {'questionnaire_list': questionnaire_list, 'exam_strings': exam_strings},
                                        request=request)
        return JsonResponse(data)

    def load_topics(self, request):
        subject_id = request.GET.get('subject')
        topics = Topics.objects.filter(subject_id=subject_id).order_by('name')
        return render(request, 'admin/exam/topic_dropdown_list_options.html', {'topic_list': topics})

    def load_sub_topics(self, request):
        topic_id = request.GET.get('topic')
        sub_topics = SubTopics.objects.filter(topics=topic_id).order_by('name')
        return render(request, 'admin/exam/sub_topic_dropdown_list_options.html', {'sub_topic_list': sub_topics})

    def load_previous_tags(self, request):
        previous_tags = list(Tag.objects.values_list('tag_name', flat=True))
        return JsonResponse(previous_tags, safe=False)

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(Exam, ExamAdmin)
admin.site.register(ExamCategory)
admin.site.register(ExamLevel)
admin.site.register(ExamQuestionnaireDetails)
