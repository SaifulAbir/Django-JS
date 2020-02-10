# Generated by Django 3.0.3 on 2020-02-10 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Division',
                'verbose_name_plural': 'Divisions',
                'db_table': 'divisions',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('division', models.ForeignKey(db_column='division', on_delete=django.db.models.deletion.PROTECT, related_name='district', to='location.Division')),
            ],
            options={
                'verbose_name': 'District',
                'verbose_name_plural': 'Districts',
                'db_table': 'districts',
            },
        ),
    ]
