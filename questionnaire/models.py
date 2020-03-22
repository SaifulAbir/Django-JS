from django.db import models
from question.models import Question, Subject, Topics, SubTopics

# Create your models here.
from resources import strings_questionnaire


class Questionnaire(models.Model):
    name = models.CharField(max_length=255, unique=True)
    remarks = models.CharField(max_length=256, null=True, blank=True)
    subject = models.ForeignKey(Subject,null=True, blank=True,on_delete=models.PROTECT)
    topic = models.ForeignKey(Topics,null=True, blank=True,on_delete=models.PROTECT)
    sub_topic = models.ForeignKey(SubTopics,null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super(Questionnaire, self).__init__( *args, **kwargs)
        self._meta.get_field('name').verbose_name = strings_questionnaire.NAME_TEXT
        self._meta.get_field('remarks').verbose_name = strings_questionnaire.REMARKS_TEXT
        self._meta.get_field('subject').verbose_name = strings_questionnaire.SUBJECT_TEXT
        self._meta.get_field('topic').verbose_name = strings_questionnaire.TOPIC_TEXT
        self._meta.get_field('sub_topic').verbose_name = strings_questionnaire.SUBTOPIC_TEXT


    class Meta:
        verbose_name = strings_questionnaire.QUESTIONNAIRE_VERBOSE_NAME_SINGLE
        verbose_name_plural = strings_questionnaire.QUESTIONNAIRE_VERBOSE_NAME_PLURAL
        db_table= 'questionnaire'




class QuestionnaireDetail(models.Model):
    questionnaire_id = models.ForeignKey(Questionnaire, on_delete=models.PROTECT)
    question_id = models.ForeignKey(Question, on_delete=models.PROTECT)



    class Meta:
        verbose_name = strings_questionnaire.QUESTIONNAIREDETAL_VERBOSE_NAME_SINGLE
        verbose_name_plural = strings_questionnaire.QUESTIONNAIREDETAIL_VERBOSE_NAME_PLURAL
        db_table='Questionnaire_details'
