from django.db import models
import uuid
# Create your models here.
from resources import strings_pro

# PROFESSIONAL MODEL
class Professional(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='id')
    professional_id = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    industry_expertise = models.CharField(max_length=255, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = strings_pro.PROFESSIONAL_VERBOSE_NAME
        verbose_name_plural = strings_pro.PROFESSIONAL_VERBOSE_NAME_PLURAL
        db_table = 'professionals'
# PROFESSIONAL MODEL