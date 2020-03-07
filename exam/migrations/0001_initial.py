# Generated by Django 3.0.3 on 2020-03-07 08:37

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Exam Category',
                'verbose_name_plural': 'Exam Categories',
                'db_table': 'exams_category',
            },
        ),
        migrations.CreateModel(
            name='ExamLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Exam Level',
                'verbose_name_plural': 'Exam Levels',
                'db_table': 'exams_level',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(blank=True, max_length=256, null=True)),
                ('tag_type', models.CharField(choices=[('exam', 'Exam'), ('questionnaire', 'Questionnaire')], max_length=50)),
                ('tags', models.CharField(blank=True, max_length=50, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'db_table': 'tags',
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_code', models.CharField(max_length=50)),
                ('exam_name', models.CharField(max_length=256)),
                ('pass_mark', models.CharField(max_length=200)),
                ('duration', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('is_featured', models.BooleanField(blank=True, default=False, null=True)),
                ('instruction', ckeditor.fields.RichTextField()),
                ('question_selection_type', models.CharField(blank=True, max_length=30, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('exam_type', models.CharField(blank=True, max_length=50, null=True)),
                ('exam_fee', models.CharField(blank=True, max_length=100, null=True)),
                ('promo_code', models.CharField(blank=True, max_length=256, null=True)),
                ('discount_price', models.CharField(blank=True, max_length=128, null=True)),
                ('discount_percent', models.CharField(blank=True, max_length=128, null=True)),
                ('re_registration_delay', models.CharField(blank=True, max_length=100, null=True)),
                ('exam_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.ExamCategory')),
                ('exam_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.ExamLevel')),
                ('sub_topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='question.SubTopics')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='question.Subject')),
                ('topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='question.Topics')),
            ],
            options={
                'verbose_name': 'Exam',
                'verbose_name_plural': 'Exams',
                'db_table': 'exams',
            },
        ),
    ]
