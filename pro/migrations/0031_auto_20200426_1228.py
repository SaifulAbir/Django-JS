# Generated by Django 3.0.3 on 2020-04-26 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pro', '0030_auto_20200426_1145'),
    ]

    operations = [
        migrations.RenameField(
            model_name='professionaleducation',
            old_name='new_major',
            new_name='major_text',
        ),
        migrations.AlterField(
            model_name='professionalskill',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
    ]
