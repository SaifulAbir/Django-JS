from django.contrib import admin

# Register your models here.
from django.forms import BaseInlineFormSet, forms
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
    list_display = ['name','subject','topic','sub_topic','remarks']
    list_filter = (('name',DropdownFilter),('subject',RelatedDropdownFilter),('topic',RelatedDropdownFilter),
                   ('sub_topic',RelatedDropdownFilter))
    inlines = [QuestionnaireDetailInline]

admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(QuestionnaireDetail, QuestionnaireDetailAdmin)
