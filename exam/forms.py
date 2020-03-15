from ckeditor.widgets import CKEditorWidget
from django import forms
# from exams.models import Exam, ExamCategory, ExamLevel
# from resources import strings
# from resources.strings import *
# from sub_topics.models import SubTopics
# from subject.models import Subject
# from topics.models import Topics
from django.utils.translation import ugettext_lazy as _
# from exams.strings import *
from exam.models import ExamCategory, ExamLevel, Exam
from question.models import Subject, Topics, SubTopics
from resources.strings_exam import *

QUESTIONNAIRE_TYPE = [(MANUAL, MANUAL_TITLE_CASE),(AUTO,AUTO_TITLE_CASE)]
EXAM_TYPE = [(PRIVATE, PRIVATE_TITLE_CASE),(PUBLIC,PUBLIC_TITLE_CASE)]





class ExamForm(forms.ModelForm):

    instruction = forms.CharField(required=False, widget=CKEditorWidget(attrs={'class':"form-control"}))
    exam_code = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':"form-control"}))
    exam_name = forms.CharField(error_messages={'required':EXAM_NAME_REQUIRED_ERROR}, widget=forms.TextInput(attrs={'class': "form-control"}))
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control", 'id': 'exam_tags'}))
    pass_mark = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    duration = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    exam_fee = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    re_registration_delay = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    discount_percent = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    promo_code = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    discount_price = forms.CharField(label=DISCOUNT_LABEL, required=False, widget=forms.TextInput(attrs={'class': "form-control"}))

    subject = forms.ModelChoiceField(required=False, queryset=Subject.objects.all(),
                                    empty_label=DROPDOWN_DEFAULT_EMPTY_STRING, widget=forms.Select(attrs={'class' : "form-control subject-dropdown"}))
    topic = forms.ModelChoiceField(required=False, queryset=Topics.objects.all(),
                                    empty_label=DROPDOWN_DEFAULT_EMPTY_STRING, widget=forms.Select(attrs={'class' : "form-control topic-dropdown"
            ,'data-text':'name',"data-value":"id","data-placeholder":"--------","data-src":"/api/topic_populate","data-parent":"#id_subject"}))
    sub_topic = forms.ModelChoiceField(required=False, queryset=SubTopics.objects.all(),
                                    empty_label=DROPDOWN_DEFAULT_EMPTY_STRING, widget=forms.Select(attrs={'class' : "form-control subtopic-dropdown"}))
    exam_category = forms.ModelChoiceField(required=False, queryset=ExamCategory.objects.all(),
                                    empty_label=DROPDOWN_DEFAULT_EMPTY_STRING, widget=forms.Select(attrs={'class' : "form-control"}))
    exam_level = forms.ModelChoiceField(required=False, queryset=ExamLevel.objects.all(),
                                    empty_label=DROPDOWN_DEFAULT_EMPTY_STRING, widget=forms.Select(attrs={'class' : "form-control"}))

    image = forms.ImageField(label=_(EXAM_THUMBNAIL), required=False,
                             error_messages={'invalid': _(ONLY_IMAGE_UPLOAD_VALIDATION_MSG)}, widget=forms.FileInput(attrs={'id': 'image', 'placeholder': 'Image'}))
    is_featured = forms.BooleanField(required=False, label=IS_FEATURED_LABEL)
    question_selection_type = forms.ChoiceField(required=False, label=LABEL_QUESTIONNAIRE_TYPE, choices=QUESTIONNAIRE_TYPE, widget=forms.RadioSelect, initial=MANUAL)
    exam_type = forms.ChoiceField(error_messages={'required':EXAM_TYPE_REQUIRED_ERROR}, choices=EXAM_TYPE, widget=forms.RadioSelect, initial=PUBLIC)

    ## Test case exist of this method. Please read and learn.
    def clean(self):
        cleaned_data = super().clean()
        discount_price = cleaned_data.get("discount_price")
        exam_fee = cleaned_data.get("exam_fee")
        discount_percent = cleaned_data.get("discount_percent")

        if discount_price and discount_percent :
            msg = ERROR_MESSAGE_FOR_DISCOUNT_PRICE_AND_DISCOUNT_PERCENTAGE_CAN_NOT_BE_APPLIED_AT_A_TIME
            self.add_error('exam_fee', msg)

        if exam_fee:
            if int(exam_fee) < 0:
                msg = NEGATIVE_VALUE_NOT_ALLOWED_ERROR
                self.add_error('exam_fee', msg)

        if discount_percent:
            if int(discount_percent) < 0:
                msg = NEGATIVE_VALUE_NOT_ALLOWED_ERROR
                self.add_error('discount_percent', msg)

        if discount_price:
            if int(discount_price) < 0:
                msg = NEGATIVE_VALUE_NOT_ALLOWED_ERROR
                self.add_error('discount_price', msg)

        if discount_percent:
            if int(discount_percent) > 100:
                msg = DEFAULT_MAX_PERCENTAGE_ERROR
                self.add_error('discount_percent', msg)

        if discount_price is not None and discount_price > exam_fee:
            msg = ERROR_MESSAGE_FOR_DISCOUNT_PRICE
            self.add_error('discount_price', msg)



    class Meta:
        model = Exam
        fields = ('exam_code', 'exam_name', 'pass_mark', 'duration', 'instruction','exam_category')

