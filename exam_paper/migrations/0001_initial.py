# Generated by Django 3.0.3 on 2020-03-15 09:37

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exam', '0002_examquestionnairedetails'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registration', '0001_initial'),
        ('question', '0001_initial'),
        ('questionnaire', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exampaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('answers_id', models.CharField(max_length=200)),
                ('submitted_ans_id', models.CharField(max_length=200)),
                ('correct', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('exam', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='exam', to='exam.Exam')),
                ('professional', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.PROTECT, to='question.Question')),
                ('registration', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='registration', to='registration.Registration')),
            ],
            options={
                'verbose_name_plural': 'Exam Paper',
                'db_table': 'exam_paper',
            },
        ),
        migrations.CreateModel(
            name='AssignQuestionnaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('professional', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='questionnaire', to='questionnaire.Questionnaire')),
            ],
            options={
                'verbose_name_plural': 'Assign Questionnaire',
            },
        ),
    ]
