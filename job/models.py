from django.db import models
from django.utils import timezone
from resources import strings_job
# Create your models here.

#Company Model
class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)



divisions = [
    'Dhaka',
    'Chittagong',
]

district = {
    'Dhaka' : ['Dhaka', ],
    'Chittagong': []
}

#Company Model


#Industry Model
class Industry(models.Model):
    name = models.CharField(max_length=128)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = strings_job.INDUSTRY_VERBOSE_NAME
        verbose_name_plural = strings_job.INDUSTRY_VERBOSE_NAME_PLURAL
        db_table = 'industry'
#Industry Model


#JobType Model
class JobType(models.Model):
    name = models.CharField(max_length=128)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = strings_job.JOB_TYPE_VERBOSE_NAME
        verbose_name_plural = strings_job.JOB_TYPE_VERBOSE_NAME_PLURAL
        db_table = 'Job_type'
#JobType Model


#Qualification Model
class Qualification(models.Model):
    name = models.CharField(max_length=128)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = strings_job.QUALIFICATION_VERBOSE_NAME
        verbose_name_plural = strings_job.QUALIFICATION_VERBOSE_NAME_PLURAL
        db_table = 'Qualification'
#Qualification Model


#Job Model
class Job(models.Model):
    name = models.CharField(max_length=128)
    industry = models.ForeignKey(Industry, on_delete=models.PROTECT,)
    job_type = models.ForeignKey(JobType, on_delete=models.PROTECT,)
    job_location = models.CharField(max_length=256)
    experience = models.CharField(max_length=128)
    salary_range = models.CharField(blank=True, null= True)
    qualification = models.ForeignKey(Qualification, on_delete=models.PROTECT )
    gender = models.CharField(max_length=128)
    descriptions = models.TextField(blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    other_benefits = models.TextField(max_length=128, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null = True)
    city = models.CharField(max_length=128, blank=True, null = True)
    zipcode = models.CharField(max_length=128, blank=True, null = True)
    comapny_location = models.CharField(max_length=128, blank=True, null = True)
    comapny_name = models.CharField(max_length=128, blank=True, null = True)
    webaddress = models.CharField(max_length=128, blank=True, null = True)


    class Meta:
        verbose_name = strings_job.JOB_VERBOSE_NAME
        verbose_name_plural = strings_job.JOB_VERBOSE_NAME_PLURAL
        db_table = 'job'
#job Model

