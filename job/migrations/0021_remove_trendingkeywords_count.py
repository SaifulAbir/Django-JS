# Generated by Django 3.0.3 on 2020-03-25 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0020_merge_20200325_0948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trendingkeywords',
            name='count',
        ),
    ]
