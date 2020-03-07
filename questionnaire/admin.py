from django.contrib import admin

# Register your models here.
from questionnaire.models import Questionnaire, QuestionnaireDetail
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

class QuestionnaireDetailAdmin(admin.ModelAdmin):
    list_display = ['questionnaire_id','question_id']

class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['name','subject','topic','sub_topic','remarks']
    list_filter = (('name',DropdownFilter),('subject',RelatedDropdownFilter),('topic',RelatedDropdownFilter),
                   ('sub_topic',RelatedDropdownFilter))

admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(QuestionnaireDetail, QuestionnaireDetailAdmin)
