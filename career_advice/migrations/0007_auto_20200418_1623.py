# Generated by Django 3.0.3 on 2020-04-18 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('career_advice', '0006_merge_20200414_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='careeradvice',
            name='author',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='careeradvice',
            name='short_description',
            field=models.CharField(max_length=250),
        ),
    ]
