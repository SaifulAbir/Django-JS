from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin import ModelAdmin, AdminSite
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from answer.models import Answer
from examinees.models import Examinee
from questionnaire.models import Questionnaire
from registration.models import Registration
from .models import Exampaper, AssignQuestionnaire
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

# Register your models here.

class QuestionnaireSubmitAdmin(ModelAdmin):

    list_display = ['question_text','answers_id','correct']
    #list_filter = [('registration_id',RelatedDropdownFilter),('question_text',DropdownFilter),('answers_id',DropdownFilter),('correct',DropdownFilter)]
    search_fields = ['question_text__icontains', 'answers_id__iexact', 'correct__iexact']

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('result_summary/', self.result_summary, name='result_summary'),
            path('assign_questionnaire_create/', self.assign_questionnaire_create, name='assign_questionnaire_create'),
            path('result_details/<int:registration_id>', self.result_details, name='result_details'),
        ]
        return my_urls + urls
    def result_summary(self, request):
        # ...
        result = []
        partial_result = Exampaper.objects.values('registration_id').annotate(
            number_of_correct=Count('correct', filter=Q(correct__gt=0),)).annotate(
            number_of_question_id=Count('question_id'))
        for full_result in partial_result:
            full_result['registration_obj'] = Registration.objects.get(pk=full_result['registration_id'])
            result.append(full_result)
        paginator = Paginator(result, 10)
        page = request.GET.get('page')
        result_list = paginator.get_page(page)
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            result = result_list
        )
        return TemplateResponse(request, "admin/questionnaire_submit_change_list.html", context)


    def result_details(self, request, registration_id):
        result_details = []
        qs = None
        total_result = Exampaper.objects.filter(registration_id=registration_id).values('registration_id').annotate(
            number_of_correct=Count('correct', filter=Q(correct__gt=0), )).annotate(
            number_of_question_id=Count('question_id'))
        result_questionnaire_submit = Exampaper.objects.filter(registration_id = registration_id)
        for question in result_questionnaire_submit:
            qs = question
            submitted_ans_list = (question.submitted_ans_id).split(',')
            result = Answer.objects.filter(question = question.question_id)
            result_details.append({'question_obj':question, 'answer_obj':result, 'submitted_ans_list':submitted_ans_list})
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            result = result_details,
            qs = qs,
            total_result = total_result
        )
        return TemplateResponse(request, "admin/result_details_list.html", context)

    def assign_questionnaire_create(self, request):
        questionnaire_list = Questionnaire.objects.all()
        examinee_list = Examinee.objects.all()
        if request.method == 'POST':
            questionnaire_id = request.POST.get('questionnaire_id')
            examinee_id_list = request.POST.getlist('examinee_id')
            for examinee_id in examinee_id_list:
                assign_questionnaire_obj = AssignQuestionnaire(questionnaire_id_id = questionnaire_id, examinee_id_id = examinee_id)
                assign_questionnaire_obj.save()
            return redirect(reverse('admin:questionnaire_submit_assignquestionnaire_changelist'))
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            questionnaire_list = questionnaire_list,
            examinee_list = examinee_list

        )

        return TemplateResponse(request, "admin/assign_questionnaire_create.html", context)


class AssignQuestionnaireAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(Exampaper, QuestionnaireSubmitAdmin)
admin.site.register(AssignQuestionnaire, AssignQuestionnaireAdmin)