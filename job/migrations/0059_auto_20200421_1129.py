# Generated by Django 3.0.3 on 2020-04-21 05:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0058_auto_20200421_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 21, 5, 29, 27, 697439, tzinfo=utc)),
        ),
    ]
