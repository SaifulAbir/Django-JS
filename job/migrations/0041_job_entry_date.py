# Generated by Django 3.0.3 on 2020-04-12 15:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0040_merge_20200412_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='entry_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
