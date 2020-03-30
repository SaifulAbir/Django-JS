from django.db import models
from resources import strings_settings


class Settings(models.Model):
    facebook_url = models.URLField(verbose_name='Facebook URL')
    linkedin_url = models.URLField(verbose_name='Linkedin URL', blank=True, null=True)
    twitter_url = models.URLField(verbose_name='Twitter URL', blank=True, null=True)
    logo_url = models.ImageField(upload_to='logo/', blank=True)

    class Meta:
        verbose_name = strings_settings.SETTINGS_VERBOSE_NAME
        verbose_name_plural = strings_settings.SETTINGS_VERBOSE_NAME_PLURAL
        db_table = 'settings'

    def __str__(self):
        return self.facebook_url
