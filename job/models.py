import uuid
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from rest_framework.utils import json

from job.utils import unique_slug_generator
from location.models import Division, District
from resources import strings_job
from django_countries.fields import CountryField
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
    profile_picture = models.ImageField(upload_to='images/', blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
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

# Added by Munir (02-03).05.2020 >>>

class JobSource(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(null=True)
    created_from = models.CharField(max_length=255, null=True)
    modified_by = models.CharField(max_length=255, null=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_from = models.CharField(max_length=255, null=True)
    is_archived = models.BooleanField(default=False)
    archived_by = models.CharField(max_length=255, null=True)
    archived_at = models.DateTimeField(null=True)
    archived_from = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = strings_job.JOBSOURCE_VERBOSE_NAME
        verbose_name_plural = strings_job.JOBSOURCE_VERBOSE_NAME_PLURAL
        db_table = 'job_sources'

    def __str__(self):
        return self.name



class JobCategory(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    created_by = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(null=True)
    created_from = models.CharField(max_length=255, null=True)
    modified_by = models.CharField(max_length=255, null=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_from = models.CharField(max_length=255, null=True)
    is_archived = models.BooleanField(default=False)
    archived_by = models.CharField(max_length=255, null=True)
    archived_at = models.DateTimeField(null=True)
    archived_from = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = strings_job.JOBCATEGORY_VERBOSE_NAME
        verbose_name_plural = strings_job.JOBCATEGORY_VERBOSE_NAME_PLURAL
        db_table = 'job_categories'

    def __str__(self):
        return self.name



class JobGender(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    created_by = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(null=True)
    created_from = models.CharField(max_length=255, null=True)
    modified_by = models.CharField(max_length=255, null=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_from = models.CharField(max_length=255, null=True)
    is_archived = models.BooleanField(default=False)
    archived_by = models.CharField(max_length=255, null=True)
    archived_at = models.DateTimeField(null=True)
    archived_from = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = strings_job.JOBGENDER_VERBOSE_NAME
        verbose_name_plural = strings_job.JOBGENDER_VERBOSE_NAME_PLURAL
        db_table = 'job_genders'

    def __str__(self):
        return self.name
# <<<

#Job Model
class Job(models.Model):
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False,db_column='id')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True,null=True, blank=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    job_area = models.CharField(max_length=255, blank=True, null = True)
    job_city = models.CharField(max_length=255, blank=True, null = True)
    job_country = CountryField(default = strings_job.DEFAULT_JOB_COUNTRY)
    salary = models.CharField(max_length=255, blank=True, null=True)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null= True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null= True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True, db_column='currency')
    other_benefits = models.TextField(max_length=255, blank=True, null=True)
    experience =  models.CharField(max_length=10, blank=True, null= True)
    description = models.TextField(blank=True, null=True)
    qualification = models.ForeignKey(Qualification, on_delete=models.PROTECT,blank=True, null= True,db_column='qualification')
    responsibilities = models.TextField(blank=True, null=True)
    additional_requirements = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    vacancy = models.PositiveIntegerField(default=1, null=True)
    application_deadline = models.DateField(null=True, blank=True)
    company_name = models.ForeignKey(Company,on_delete=models.PROTECT, db_column='company', related_name='jobs')
    company_profile = models.TextField(blank=True, null = True)
    company_address = models.CharField(max_length=255, blank=True, null = True)
    company_area = models.CharField(max_length=255, blank=True, null = True)
    company_city = models.CharField(max_length=255, blank=True, null = True)
    company_country = CountryField(default = strings_job.DEFAULT_JOB_COUNTRY)
    latitude = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null = True)
    longitude = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null = True)
    raw_content = models.TextField(blank=True, null=True)
    favorite_count = models.PositiveIntegerField(default=0)
    applied_count = models.PositiveIntegerField(default=0)
    terms_and_condition = models.BooleanField(default=False)
    job_skills = models.ManyToManyField('Skill', blank=True, related_name='skill_set')
    status = models.CharField(max_length=20, blank=False, null = False,
        choices=strings_job.JOB_STATUSES, default=strings_job.DEFAULT_JOB_STATUS)
    job_site = models.CharField(max_length=20, blank=False, null = False, 
        choices=strings_job.JOB_SITES, default=strings_job.DEFAULT_JOB_SITE)
    job_nature = models.CharField(max_length=20, blank=False, null = False, 
        choices=strings_job.JOB_NATURES, default=strings_job.DEFAULT_JOB_NATURE)
    job_type = models.CharField(max_length=20, blank=False, null = False, 
        choices=strings_job.JOB_TYPES, default=strings_job.DEFAULT_JOB_TYPE)
    creator_type = models.CharField(max_length=20, blank=False, null = False, 
        choices=strings_job.JOB_CREATOR_TYPES, default=strings_job.DEFAULT_JOB_CREATOR_TYPE)
    job_source_1 = models.ForeignKey(JobSource, on_delete=models.PROTECT,
        related_name='jobs1', db_column='job_source_1', blank=True, null= True)
    job_url_1 = models.CharField(max_length=255, blank=True, null= True)
    job_source_2 = models.ForeignKey(JobSource, on_delete=models.PROTECT, 
        related_name='jobs2', db_column='job_source_2', blank=True, null= True)
    job_url_2 = models.CharField(max_length=255, blank=True, null= True)
    job_source_3 = models.ForeignKey(JobSource, on_delete=models.PROTECT, 
        related_name='jobs3', db_column='job_source_3',blank=True, null = True)
    job_url_3 = models.CharField(max_length=255, blank=True, null= True)
    job_category = models.ForeignKey(JobCategory, on_delete=models.PROTECT,
        related_name='jobs', db_column='job_category',blank=True, null = True)
    job_gender = models.ForeignKey(JobGender, on_delete=models.PROTECT,
        related_name='jobs', db_column='job_gender',blank=True, null = True)
    post_date = models.DateTimeField(blank=True, null = True)
    review_date = models.DateTimeField(blank=True, null = True)
    approve_date = models.DateTimeField(blank=True, null = True)
    publish_date = models.DateTimeField(blank=True, null = True)
    created_by = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(null=True)
    created_from = models.CharField(max_length=255, null=True)
    modified_by = models.CharField(max_length=255, null=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_from = models.CharField(max_length=255, null=True)
    is_archived = models.BooleanField(default=False)
    archived_by = models.CharField(max_length=255, null=True)
    archived_at = models.DateTimeField(null=True)
    archived_from = models.CharField(max_length=255, null=True)


    class Meta:
        verbose_name = strings_job.JOB_VERBOSE_NAME
        verbose_name_plural = strings_job.JOB_VERBOSE_NAME_PLURAL
        db_table = 'jobs'
        ordering = ['-post_date']

    def load_data(self, json_data):
        self.__dict__ = json_data

    def __str__(self):
        return self.title



def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Job)
#job Model



class Skill(models.Model):
    name = models.CharField(max_length=255,unique=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = strings_job.SKILLS_VERBOSE_NAME
        verbose_name_plural = strings_job.SKILLS_VERBOSE_NAME_PLURAL
        db_table = 'skills'

    def __str__(self):
        return self.name

# class JobsJobSkills(models.Model):
#     job = models.ForeignKey('Jobs', models.DO_NOTHING)
#     skill = models.ForeignKey('Skills', models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'jobs_job_skills'
#         unique_together = (('job', 'skill'),)



#Trending Keywords Model Starts here
class TrendingKeywords(models.Model):
    keyword = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    device = models.CharField(max_length=255, default='Unknown')
    browser = models.CharField(max_length=255,default='Unknown')
    operating_system = models.CharField(max_length=255,default='Unknown')
    created_date = models.DateTimeField(default=timezone.now)

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('keyword') and not cleaned_data.get('location'):  # This will check for None or Empty
            raise ValidationError({'keyword': 'Even one of keyword or location should have a value.'})

    class Meta:
        verbose_name = strings_job.TRENDING_KEYWORDS_VERBOSE_NAME
        verbose_name_plural = strings_job.TRENDING_KEYWORDS_VERBOSE_NAME_PLURAL
        db_table = 'trending_keywords'

    def __str__(self):
        return self.keyword
#Trending Keywords Model ends here


#Bookmark job Model Starts here
class FavouriteJob(models.Model):
    job = models.ForeignKey(Job, on_delete=models.PROTECT, db_column='job', related_name='fav_jobs')
    user = models.ForeignKey(User, on_delete=models.PROTECT, db_column='user')
    created_date = models.DateField(default=datetime.date.today)

    class Meta:
        verbose_name = strings_job.BOOKMARK_JOB_VERBOSE_NAME
        verbose_name_plural = strings_job.BOOKMARK_JOB_VERBOSE_NAME_PLURAL
        db_table = 'favourite_jobs'

    def __str__(self):
        return self.job.title
#Bookmark job Model ends here

#Apply Online Model Starts here
class ApplyOnline(models.Model):
    job = models.ForeignKey(Job, on_delete=models.PROTECT, db_column='job')
    created_by = models.ForeignKey(User, related_name='Apply_created_by', on_delete=models.PROTECT, db_column='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    created_from = models.CharField(max_length=255)
    modified_by = models.ForeignKey(User, related_name='Apply_modified_by', on_delete=models.PROTECT, db_column='modified_by')
    modified_at = models.DateTimeField(auto_now=True)
    modified_from = models.CharField(max_length=255)

    class Meta:
        verbose_name = strings_job.APPLY_ONLINE_JOB_VERBOSE_NAME
        verbose_name_plural = strings_job.APPLY_ONLINE_JOB_VERBOSE_NAME_PLURAL
        db_table = 'apply_onlines'

    def __str__(self):
        return self.job.title
#Apply Online Model ends here

def populate_user_info(sender, instance, *args, **kwargs):
    if instance._state.adding:
        instance.created_at = timezone.now()
    else:
        instance.modified_at = timezone.now()
        if instance.is_archived and not instance.archived_at:
            instance.archived_at = timezone.now()
    print(instance._state.adding)

pre_save.connect(populate_user_info, sender=JobCategory)
pre_save.connect(populate_user_info, sender=JobSource)
pre_save.connect(populate_user_info, sender=JobGender)

