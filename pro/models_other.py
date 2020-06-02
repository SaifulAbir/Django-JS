import datetime

from django.contrib.auth.models import User
from django.db import models
import uuid
# Create your models here.
from django.utils import timezone

from job.models import Industry, Gender, JobType, Experience, Qualification, Company, Skill
from p7.validators import check_valid_password, MinLengthValidator, \
    check_valid_phone_number
from pro.models import Professional
from resources import strings_pro


class Nationality(models.Model):
    name = models.CharField(max_length=255, )
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'nationalities'


class Institute(models.Model):
    name = models.CharField(max_length=255, )
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'institutes'


class Organization(models.Model):
    name = models.CharField(max_length=255, )
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'organizations'



class Major(models.Model):
    name = models.CharField(max_length=255, )
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'majors'

class Religion(models.Model):
    name = models.CharField(max_length=255, )
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'religions'


class ProfessionalEducation(models.Model):
    professional = models.ForeignKey(Professional,on_delete=models.PROTECT)
    degree = models.ForeignKey(Qualification, on_delete=models.PROTECT) # name = degree
    institution = models.ForeignKey(Institute, on_delete=models.PROTECT, null=True, blank=True)
    institution_text = models.CharField(max_length=255,blank=True, null=True)
    cgpa = models.CharField(max_length=255, blank=True, null=True)
    major = models.ForeignKey(Major, on_delete=models.PROTECT, null=True, blank=True)
    major_text = models.CharField(max_length=255,blank=True, null=True)
    is_ongoing = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    enrolled_date = models.DateField(null=True, blank=True)
    graduation_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='education_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='education_modified_by')
    created_at = models.CharField(max_length=255,blank=True, null=True)
    modified_at = models.CharField(max_length=255,blank=True, null=True)
    is_archived = models.BooleanField(default=False)


    class Meta:
        db_table = 'professional_educations'


class ProfessionalSkill(models.Model):
    professional = models.ForeignKey(Professional, on_delete=models.PROTECT)
    skill_name = models.ForeignKey(Skill, on_delete=models.PROTECT)
    rating = models.DecimalField(default=0, decimal_places=2,max_digits=4)
    verified_by_skillcheck = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='skill_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='skill_modified_by')
    created_at = models.CharField(max_length=255, blank=True, null=True)
    modified_at = models.CharField(max_length=255, blank=True, null=True)
    is_archived = models.BooleanField(default=False)


    class Meta:
        db_table = 'professional_skills'


class WorkExperience(models.Model):
    professional = models.ForeignKey(Professional,on_delete=models.PROTECT)
    company_text = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.PROTECT ,blank=True, null=True, related_name='company_pic')
    designation = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='experience_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='experience_modified_by')
    created_at = models.CharField(max_length=255, blank=True, null=True)
    modified_at = models.CharField(max_length=255, blank=True, null=True)
    is_archived = models.BooleanField(default=False)
    is_currently_working = models.BooleanField(default=False)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'work_experiences'


class Portfolio(models.Model):
    professional = models.ForeignKey(Professional,on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    image = models.CharField(blank=True, null=True, max_length=500)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='portfolio_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='portfolio_modified_by')
    created_at = models.CharField(max_length=255, blank=True, null=True)
    modified_at = models.CharField(max_length=255, blank=True, null=True)
    is_archived = models.BooleanField(default=False)



    class Meta:
        db_table = 'portfolios'

class Membership(models.Model):
    professional = models.ForeignKey(Professional,on_delete=models.PROTECT)
    organization = models.CharField(max_length=255)
    position_held = models.CharField(max_length=255, blank=True, null=True)
    membership_ongoing = models.BooleanField(default=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='membership_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='membership_modified_by')
    created_at = models.CharField(max_length=255, blank=True, null=True)
    modified_at = models.CharField(max_length=255, blank=True, null=True)
    is_archived = models.BooleanField(default=False)


    class Meta:
        db_table = 'memberships'


class CertificateName(models.Model):
    name = models.CharField(max_length=255)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'certificate_names'


class Certification(models.Model):
    professional = models.ForeignKey(Professional,on_delete=models.PROTECT)
    certificate_name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255,blank=True, null=True)
    has_expiry_period = models.BooleanField(default=True)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=255,null=True, blank=True)
    credential_url = models.CharField(max_length=255,null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='certification_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='certification_modified_by')
    created_at = models.CharField(max_length=255, blank=True, null=True)
    modified_at = models.CharField(max_length=255, blank=True, null=True)
    is_archived = models.BooleanField(default=False)


    class Meta:
        db_table = 'certifications'



class Reference(models.Model):
    professional = models.ForeignKey(Professional,on_delete=models.PROTECT)
    description = models.TextField(blank=False,null=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='reference_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='reference_modified_by')
    created_at = models.CharField(max_length=255, blank=True, null=True)
    modified_at = models.CharField(max_length=255, blank=True, null=True)
    is_archived = models.BooleanField(default=False)



    class Meta:
        db_table= 'references'



class ProRecentActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    description = description = models.TextField(blank=False,null=False)
    time =  models.DateTimeField(default=timezone.now)
    type =  models.CharField(max_length=255,null=True,blank=True)
    created_by = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_from = models.CharField(max_length=255, null=True)
    modified_by = models.CharField(max_length=255, null=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_from = models.CharField(max_length=255, null=True)
    is_archived = models.BooleanField(default=False)
    archived_by = models.CharField(max_length=255, null=True)
    archived_at = models.DateTimeField(null=True)
    archived_from = models.CharField(max_length=255, null=True)







