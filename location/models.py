from django.db import models
from resources import strings_location

# Create your models here.

class Division(models.Model):
    name = models.CharField(max_length=255, primary_key=True)

    class Meta:
        verbose_name = strings_location.DIVISION_VERBOSE_NAME
        verbose_name_plural = strings_location.DIVISION_VERBOSE_NAME_PLURAL
        db_table = 'divisions'

class District(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    division = models.ForeignKey(Division, related_name='district', on_delete=models.PROTECT, db_column='division')

    class Meta:
        verbose_name = strings_location.DISTRICT_VERBOSE_NAME
        verbose_name_plural = strings_location.DISTRICT_VERBOSE_NAME_PLURAL
        db_table = 'districts'