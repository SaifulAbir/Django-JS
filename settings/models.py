from django.db import models
from resources import strings_settings


class Settings(models.Model):
    facebook_url = models.URLField(verbose_name='Facebook URL')
    linkedin_url = models.URLField(verbose_name='Linkedin URL', blank=True, null=True)
    twitter_url = models.URLField(verbose_name='Twitter URL', blank=True, null=True)
    appstore_url = models.URLField(verbose_name='App Store URL', blank=True, null=True)
    playstore_url = models.URLField(verbose_name='Play Store URL', blank=True, null=True)
    logo_url = models.ImageField(upload_to='logo/', blank=True)
    admin_email = models.CharField(max_length=20)
    support_email = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=11)
    zoom = models.DecimalField(max_digits=2, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)

    class Meta:
        verbose_name = strings_settings.SETTINGS_VERBOSE_NAME
        verbose_name_plural = strings_settings.SETTINGS_VERBOSE_NAME_PLURAL
        db_table = 'settings'

    def __str__(self):
        return self.facebook_url
