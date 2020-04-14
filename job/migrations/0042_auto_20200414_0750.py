# Generated by Django 3.0.3 on 2020-04-14 07:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job', '0041_applyonline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applyonline',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='applyonline',
            name='user',
        ),
        migrations.AddField(
            model_name='applyonline',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='applyonline',
            name='created_by',
            field=models.ForeignKey(db_column='created_by', default='', on_delete=django.db.models.deletion.PROTECT, related_name='Apply_created_by', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='applyonline',
            name='created_from',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='applyonline',
            name='modified_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='applyonline',
            name='modified_by',
            field=models.ForeignKey(db_column='modified_by', default='', on_delete=django.db.models.deletion.PROTECT, related_name='Apply_modified_by', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='applyonline',
            name='modified_from',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
