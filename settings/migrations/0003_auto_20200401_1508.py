# Generated by Django 3.0.3 on 2020-04-01 09:08

import datetime
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_auto_20200328_0635'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='appstore_url',
            field=models.URLField(default=datetime.datetime(2020, 4, 1, 9, 8, 23, 443124, tzinfo=utc), verbose_name='App Store URL'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='settings',
            name='playstore_url',
            field=models.URLField(default=django.utils.timezone.now, verbose_name='Play Store URL'),
            preserve_default=False,
        ),
    ]
