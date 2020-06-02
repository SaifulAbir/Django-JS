import datetime

from django.contrib.auth.models import User
from django.db import models
import uuid
# Create your models here.
from django.utils import timezone

from job.models import Industry, Gender, JobType, Experience, Qualification, Company, Skill
from p7.validators import check_valid_password, MinLengthValidator, \
    check_valid_phone_number
from pro.models_other import Nationality, Religion
from resources import strings_pro


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
    facebook_id= models.CharField(max_length=255, blank=True, null=True)
    twitter_id= models.CharField(max_length=255, blank=True, null=True)
    linkedin_id= models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(default=datetime.date.today)
    blood_group = models.CharField(max_length=5, null=True, blank=True)
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
    current_company = models.CharField(max_length=255, null=True, blank=True)
    current_designation = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True,related_name='professional_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True,related_name='professional_modified_by')
    created_at = models.CharField(max_length=255, blank=True, null=True)
    modified_at = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = strings_pro.PROFESSIONAL_VERBOSE_NAME
        verbose_name_plural = strings_pro.PROFESSIONAL_VERBOSE_NAME_PLURAL
        db_table = 'professionals'



