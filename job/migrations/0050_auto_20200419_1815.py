# Generated by Django 3.0.3 on 2020-04-19 12:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0049_merge_20200419_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 19, 12, 15, 43, 486874, tzinfo=utc)),
        ),
    ]
