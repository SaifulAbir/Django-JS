from ckeditor.fields import RichTextField
from django.db import models
from datetime import datetime
from resources import strings_question
from django.utils.safestring import mark_safe

# Create your models here.


#Subject Model Starts
class Subject(models.Model):
    name = models.CharField(max_length=250, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Subject"
        db_table='subject'

#Subject Model Ends

#Topics Model Starts

class Topics(models.Model):
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject')
    name = models.CharField(max_length=250)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Topics"
        db_table= 'topics'

#Topics Model Ends

#SubTopic Model Starts

class SubTopics(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    topics = models.ForeignKey(Topics, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Sub Topics"
        db_table='subtopics'

#SubTopic Model  Ends

#Difficulty Model Starts

class Difficulty(models.Model):
    name = models.CharField(max_length=250)
    created_date = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Difficulties"
        db_table='difficulties'

#Difficulty Model Ends

#Question Types Model Starts

class QuestionType(models.Model):
    name = models.CharField(max_length=250)
    created_date = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Question types"
        db_table='question_types'

#Question Types Model Ends

#Question Model Starts

CHOICES=(
    (strings_question.QUESTION_STATUS_PUBLISHED, strings_question.QUESTION_STATUS_PUBLISHED_TEXT),
    (strings_question.QUESTION_STATUS_DRAFT, strings_question.QUESTION_STATUS_DRAFT_TEXT),
    (strings_question.QUESTION_STATUS_REJECTED, strings_question.QUESTION_STATUS_REJECTED_TEXT),
)


class Question(models.Model):
    question = RichTextField()
    question_id = models.CharField(max_length=200, default='null', null=True, blank=True)
    qtype = models.ForeignKey(QuestionType, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, null=True, blank=True)
    sub_topic = models.ForeignKey(SubTopics, on_delete=models.CASCADE, null=True, blank=True)
    difficulties = models.ForeignKey(Difficulty, on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.CharField(max_length=100, choices=CHOICES, default='2')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "Question"
        db_table= 'questions'

    def question_text(self):
        from django.utils.safestring import mark_safe
        return mark_safe(self.question)
    question_text.short_description = 'Question'


#Question Model Ends

#Answer MOdel Starts

class Answer(models.Model):
    name = models.TextField()
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    correct = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return '%d: %s' % (self.id, self.name)

    def question_field(self):
        return mark_safe(self.question)

    question_field.short_description = 'Question'

    class Meta:
        verbose_name_plural = "Answer"
        db_table='answers'

#Answer MOdel Ends