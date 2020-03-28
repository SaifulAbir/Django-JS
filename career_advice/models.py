from resources import strings_job
from django.db import models
from django.utils import timezone


# Create your models here.



#Career_Advice Model#
class CareerAdvice(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=255)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = strings_job.CAREER_VERBOSE_NAME
        verbose_name_plural = strings_job.CAREER_VERBOSE_NAME_PLURAL
        db_table = 'career_advices'

    def __str__(self):
        return self.title
#Career_Advice Model#
