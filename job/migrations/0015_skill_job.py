# Generated by Django 3.0.3 on 2020-03-23 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0014_skill'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='job',
            field=models.ForeignKey(db_column='job', default='', on_delete=django.db.models.deletion.PROTECT, to='job.Job'),
            preserve_default=False,
        ),
    ]
