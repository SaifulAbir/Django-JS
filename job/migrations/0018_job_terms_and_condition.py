# Generated by Django 3.0.3 on 2020-03-24 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0017_auto_20200323_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='terms_and_condition',
            field=models.BooleanField(default=False),
        ),
    ]
