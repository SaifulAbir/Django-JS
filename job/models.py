import uuid
import datetime
from django.db import models
from django.utils import timezone

from location.models import Division, District
from resources import strings_job
# Create your models here.

#Company Model
class Company(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    company_name_bdjobs = models.CharField(max_length=255, blank=True, null=True)
    company_name_facebook = models.CharField(max_length=255, blank=True, null=True)
    company_name_google = models.CharField(max_length=255, blank=True, null=True)
    basis_membership_no = models.CharField(max_length=50, blank=True, null=True)
    year_of_eastablishment = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    post_code = models.PositiveSmallIntegerField(null=True, blank=True)
    company_contact_no_one = models.CharField(max_length=50, blank=True, null=True)
    company_contact_no_two = models.CharField(max_length=50, blank=True, null=True)
    company_contact_no_three = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    web_address = models.CharField(max_length=255, blank=True, null=True)
    organization_head = models.CharField(max_length=60, blank=True, null=True)
    organization_head_designation =  models.CharField(max_length=30, null=True, blank=True)
    organization_head_number = models.CharField(max_length=15, null=True, blank=True)
    legal_structure_of_this_company = models.CharField(max_length=60, null=True, blank=True)
    total_number_of_human_resources = models.PositiveSmallIntegerField(null=True, blank=True)
    no_of_it_resources = models.PositiveSmallIntegerField(null=True, blank=True)
    division = models.ForeignKey(Division, on_delete=models.PROTECT, blank=True, null=True, db_column='division')
    district = models.ForeignKey(District, on_delete=models.PROTECT, blank=True, null=True,db_column='district')
    contact_person = models.CharField(max_length=50, blank=True, null=True)
    contact_person_designation = models.CharField(max_length=50, blank=True, null=True) ## need to recheck (foreign key)
    contact_person_mobile_no = models.CharField(max_length=20, blank=True, null=True)
    contact_person_email = models.CharField(max_length=100, blank=True, null=True)
    company_profile = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = strings_job.COMPANY_VERBOSE_NAME
        verbose_name_plural = strings_job.COMPANY_VERBOSE_NAME_PLURAL
        db_table = 'companies'


    def load_data(self, json_data):
        self.__dict__ = json_data

    def __str__(self):
        return self.name

#Company Model


#Industry Model
class Industry(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = strings_job.INDUSTRY_VERBOSE_NAME
        verbose_name_plural = strings_job.INDUSTRY_VERBOSE_NAME_PLURAL
        db_table = 'industries'

    def __str__(self):
        return self.name
#Industry Model


#JobType Model
class JobType(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = strings_job.JOB_TYPE_VERBOSE_NAME
        verbose_name_plural = strings_job.JOB_TYPE_VERBOSE_NAME_PLURAL
        db_table = 'job_types'

    def __str__(self):
        return self.name
#JobType Model


#Qualification Model
class Qualification(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = strings_job.QUALIFICATION_VERBOSE_NAME
        verbose_name_plural = strings_job.QUALIFICATION_VERBOSE_NAME_PLURAL
        db_table = 'qualifications'

    def __str__(self):
        return self.name
#Qualification Model


#Experience Model
class Experience(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = strings_job.EXPERIENCE_VERBOSE_NAME
        verbose_name_plural = strings_job.EXPERIENCE_VERBOSE_NAME_PLURAL
        db_table = 'experiences'

    def __str__(self):
        return self.name
#Experience Model

#Gender Model
class Gender(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = strings_job.GENDER_VERBOSE_NAME
        verbose_name_plural = strings_job.GENDER_VERBOSE_NAME_PLURAL
        db_table = 'genders'

    def __str__(self):
        return self.name
#Gender Model

#Currency Model
class Currency(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = strings_job.CURRENCY_VERBOSE_NAME
        verbose_name_plural = strings_job.CURRENCY_VERBOSE_NAME_PLURAL
        db_table = 'currencies'

    def __str__(self):
        return self.name
#Currency Model


#Job Model
class Job(models.Model):
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False,db_column='id')
    title = models.CharField(max_length=255)
    industry = models.ForeignKey(Industry, on_delete=models.PROTECT,blank=True, null= True,db_column='industry')
    employment_status = models.ForeignKey(JobType, on_delete=models.PROTECT,blank=True, null= True,db_column='employment_status')
    job_location = models.CharField(max_length=255, blank=True,null=True)
    experience =  models.ForeignKey(Experience, on_delete=models.PROTECT,blank=True, null= True,db_column='experience')
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null= True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null= True)
    qualification = models.ForeignKey(Qualification, on_delete=models.PROTECT,blank=True, null= True,db_column='qualification')
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT,blank=True, null= True,db_column='gender' )
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True, db_column='currency')
    vacancy = models.PositiveIntegerField(default=0)
    application_deadline = models.DateField(null=True, blank=True)
    descriptions = models.TextField(blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    salary = models.CharField(max_length=255, blank=True, null=True)
    other_benefits = models.TextField(max_length=255, blank=True, null=True)
    company_name = models.ForeignKey(Company,on_delete=models.PROTECT, blank=True, null = True, db_column='company')
    division = models.ForeignKey(Division,on_delete=models.PROTECT, blank=True, null = True,db_column='division')
    district = models.ForeignKey(District,on_delete=models.PROTECT, blank=True, null = True, db_column='district')
    zipcode = models.CharField(max_length=255, blank=True, null = True)
    company_location = models.CharField(max_length=255, blank=True, null = True)
    company_profile = models.CharField(max_length=255, blank=True, null = True)
    latitude = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null = True)
    longitude = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null = True)
    raw_content = models.TextField(blank=True, null=True)
    web_address = models.CharField(max_length=255, blank=True, null = True)
    terms_and_condition = models.BooleanField(default=False)
    created_date = models.DateField(default=datetime.date.today)


    class Meta:
        verbose_name = strings_job.JOB_VERBOSE_NAME
        verbose_name_plural = strings_job.JOB_VERBOSE_NAME_PLURAL
        db_table = 'jobs'

    def load_data(self, json_data):
        self.__dict__ = json_data

    def __str__(self):
        return self.title

#job Model ends here



class Skill(models.Model):
    name = models.CharField(max_length=255,unique=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = strings_job.SKILLS_VERBOSE_NAME
        verbose_name_plural = strings_job.SKILLS_VERBOSE_NAME_PLURAL
        db_table = 'skills'

    def __str__(self):
        return self.name

class Job_skill_detail(models.Model):
    job = models.ForeignKey(Job, on_delete=models.PROTECT, db_column='job')
    skill = models.ForeignKey(Skill, on_delete=models.PROTECT, db_column='skill')

    class Meta:
        verbose_name = strings_job.JOB_SKILL_DETAIL_VERBOSE_NAME
        verbose_name_plural = strings_job.JOB_SKILL_DETAIL_VERBOSE_NAME_PLURAL
        db_table = 'job_skill_details'

    def __str__(self):
        return self.job.title



#Trending Keywords Model Starts here
class TrendingKeywords(models.Model):
    keyword = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=1)
    created_date = models.DateField(default=datetime.date.today)

    class Meta:
        verbose_name = strings_job.TRENDING_KEYWORDS_VERBOSE_NAME
        verbose_name_plural = strings_job.TRENDING_KEYWORDS_VERBOSE_NAME_PLURAL
        db_table = 'trending_keywords'

    def __str__(self):
        return self.keyword
#Trending Keywords Model ends here
