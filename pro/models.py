import datetime

from django.contrib.auth.models import User
from django.db import models
import uuid
# Create your models here.
from django.utils import timezone

from job.models import Industry, Gender, JobType, Experience, Qualification, Company, Skill
from p7.validators import check_valid_password, MinLengthValidator, \
    check_valid_phone_number
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





# PROFESSIONAL MODEL
class Professional(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='id')
    professional_id = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255, validators=[check_valid_phone_number])
    address = models.CharField(max_length=255, null=True, blank=True)
    industry_expertise = models.ForeignKey(Industry, on_delete=models.PROTECT, blank=True, null= True)
    about_me = models.TextField(null=True, blank=True)
    image = models.CharField(blank=True, null=True, max_length=500)
    terms_and_condition_status = models.BooleanField(default=False)
    password = models.CharField(max_length=255, validators=[check_valid_password, MinLengthValidator(8)])
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    signup_verification_code = models.CharField(max_length=200, blank=True, null=True)
    job_alert_status = models.BooleanField(default=False)

    father_name= models.CharField(max_length=255, blank=True, null=True)
    mother_name= models.CharField(max_length=255, blank=True, null=True)
    facebbok_id= models.CharField(max_length=255, blank=True, null=True)
    twitter_id= models.CharField(max_length=255, blank=True, null=True)
    linkedin_id= models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(default=datetime.date.today)
    gender = models.ForeignKey(Gender,on_delete=models.PROTECT, null=True, blank=True)
    status = models.ForeignKey(JobType,on_delete=models.PROTECT, null=True, blank=True)
    experience = models.ForeignKey(Experience,on_delete=models.PROTECT, null=True, blank=True)
    qualification = models.ForeignKey(Qualification,on_delete=models.PROTECT, null=True, blank=True)
    expected_salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    expected_salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    nationality = models.ForeignKey(Nationality,on_delete=models.PROTECT, null=True, blank=True)
    religion = models.ForeignKey(Religion,on_delete=models.PROTECT, null=True, blank=True)
    permanent_address = models.CharField(max_length=255, null=True, blank=True)
    current_location = models.CharField(max_length=255, null=True, blank=True)








    def __str__(self):
        return self.full_name


    class Meta:
        verbose_name = strings_pro.PROFESSIONAL_VERBOSE_NAME
        verbose_name_plural = strings_pro.PROFESSIONAL_VERBOSE_NAME_PLURAL
        db_table = 'professionals'




class ProfessionalEducation(models.Model):
    professional = models.ForeignKey(Professional,on_delete=models.PROTECT)
    qualification = models.ForeignKey(Qualification, on_delete=models.PROTECT)
    institution = models.ForeignKey(Institute, on_delete=models.PROTECT, null=True, blank=True)
    cgpa = models.CharField(max_length=255, blank=True, null=True)
    major = models.ForeignKey(Major, on_delete=models.PROTECT, null=True, blank=True)
    enrolled_date = models.DateField(null=True, blank=True)
    graduation_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    is_archived = models.BooleanField(default=False)


    class Meta:
        db_table = 'professional_educations'


class ProfessionalSkill(models.Model):
    professional = models.ForeignKey(Professional, on_delete=models.PROTECT)
    name = models.ForeignKey(Skill, on_delete=models.PROTECT)
    rating = models.IntegerField(default=0)
    verified_by_skillcheck = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    is_archived = models.BooleanField(default=False)


    class Meta:
        db_table = 'professional_skills'


class WorkExperience(models.Model):
    professional = models.ForeignKey(Professional,on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    designation = models.CharField(max_length=255, blank=True, null=True)
    Started_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    is_archived = models.BooleanField(default=False)
    currently_working_here = models.BooleanField(default=False)


    class Meta:
        db_table = 'work_experiences'

class Portfolio(models.Model):
    professional = models.ForeignKey(Professional,on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    image = models.CharField(blank=True, null=True, max_length=500)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    is_archived = models.BooleanField(default=False)



    class Meta:
        db_table = 'portfolios'

class Membership(models.Model):
    professional = models.ForeignKey(Professional,on_delete=models.PROTECT)
    org_name = models.ForeignKey(Organization,on_delete=models.PROTECT)
    position_held = models.CharField(max_length=255, blank=True, null=True)
    membership_ongoing = models.BooleanField(default=False)
    Start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    desceription = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
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
    certification_name = models.ForeignKey(CertificateName,on_delete=models.PROTECT)
    organization_name = models.ForeignKey(Organization,on_delete=models.PROTECT)
    has_expiry_period = models.BooleanField(default=True)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=255,null=True, blank=True)
    credential_url = models.CharField(max_length=255,null=True, blank=True)
    is_archived = models.BooleanField(default=False)


    class Meta:
        db_table = 'certifications'



class Reference(models.Model):
    professional = models.ForeignKey(Professional,on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    current_position = models.CharField(max_length=255,null=True, blank=True)
    email = models.CharField(max_length=255,null=True, blank=True)
    mobile = models.CharField(max_length=255,null=True, blank=True, validators=[check_valid_phone_number])
    is_archived = models.BooleanField(default=False)



    class Meta:
        db_table= 'references'






