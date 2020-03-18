import datetime

from django.contrib.auth.models import User
from django.db import models
import uuid
# Create your models here.
from django.utils import timezone

from job.models import Industry
from p7.validators import check_valid_password, MinLengthValidator, \
    check_valid_phone_number
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
    signup_verification_code = models.CharField(max_length=10, blank=True, null=True)


    class Meta:
        verbose_name = strings_pro.PROFESSIONAL_VERBOSE_NAME
        verbose_name_plural = strings_pro.PROFESSIONAL_VERBOSE_NAME_PLURAL
        db_table = 'professionals'