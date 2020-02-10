import uuid

from django.db import models
from django.utils import timezone
from rest_framework.utils import json

from location.models import Division, District
from resources import strings_job
# Create your models here.

#Company Model
class Company(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    web_address = models.CharField(max_length=255, blank=True, null=True)
    division = models.ForeignKey(Division, on_delete=models.PROTECT, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = strings_job.COMPANY_VERBOSE_NAME
        verbose_name_plural = strings_job.COMPANY_VERBOSE_NAME_PLURAL
        db_table = 'company'


    def load_data(self, json_data):
        self.__dict__ = json_data

#Company Model


#Industry Model
class Industry(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = strings_job.INDUSTRY_VERBOSE_NAME
        verbose_name_plural = strings_job.INDUSTRY_VERBOSE_NAME_PLURAL
        db_table = 'industry'
#Industry Model


#JobType Model
class JobType(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = strings_job.JOB_TYPE_VERBOSE_NAME
        verbose_name_plural = strings_job.JOB_TYPE_VERBOSE_NAME_PLURAL
        db_table = 'job_type'
#JobType Model


#Qualification Model
class Qualification(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = strings_job.QUALIFICATION_VERBOSE_NAME
        verbose_name_plural = strings_job.QUALIFICATION_VERBOSE_NAME_PLURAL
        db_table = 'qualification'
#Qualification Model


#Experience Model
class Experience(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = strings_job.EXPERIENCE_VERBOSE_NAME
        verbose_name_plural = strings_job.EXPERIENCE_VERBOSE_NAME_PLURAL
        db_table = 'experience'
#Experience Model

#Gender Model
class Gender(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = strings_job.GENDER_VERBOSE_NAME
        verbose_name_plural = strings_job.GENDER_VERBOSE_NAME_PLURAL
        db_table = 'gender'
#Gender Model



#Job Model
class Job(models.Model):
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=255, blank=True,null=True)
    industry = models.ForeignKey(Industry, on_delete=models.PROTECT,blank=True, null= True,)
    employment_status = models.ForeignKey(JobType, on_delete=models.PROTECT,blank=True, null= True,)
    job_location = models.CharField(max_length=255, blank=True,null=True)
    experience =  models.ForeignKey(Experience, on_delete=models.PROTECT,blank=True, null= True,)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null= True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null= True)
    qualification = models.ForeignKey(Qualification, on_delete=models.PROTECT,blank=True, null= True, )
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT,blank=True, null= True, )
    application_deadline = models.DateField(null=True, blank=True)
    descriptions = models.TextField(blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    other_benefits = models.TextField(max_length=255, blank=True, null=True)
    comapny_name = models.ForeignKey(Company,on_delete=models.PROTECT, blank=True, null = True)
    division = models.ForeignKey(Division,on_delete=models.PROTECT, blank=True, null = True)
    district = models.ForeignKey(District,on_delete=models.PROTECT, blank=True, null = True)
    zipcode = models.CharField(max_length=255, blank=True, null = True)
    comapny_location = models.CharField(max_length=255, blank=True, null = True)
    latitude = models.CharField(max_length=255, blank=True, null = True)
    longitude = models.CharField(max_length=255, blank=True, null = True)
    web_address = models.CharField(max_length=255, blank=True, null = True)
    created_date = models.DateTimeField(default=timezone.now)


    class Meta:
        verbose_name = strings_job.JOB_VERBOSE_NAME
        verbose_name_plural = strings_job.JOB_VERBOSE_NAME_PLURAL
        db_table = 'job'
#job Model

