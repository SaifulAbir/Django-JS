# Generated by Django 3.0.3 on 2020-04-18 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0029_merge_20200405_1001'),
        ('pro', '0025_auto_20200418_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professionaleducation',
            name='qualification',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='job.Qualification'),
            preserve_default=False,
        ),
    ]
