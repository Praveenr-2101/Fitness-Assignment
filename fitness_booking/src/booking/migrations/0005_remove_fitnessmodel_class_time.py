# Generated by Django 5.2.2 on 2025-06-08 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_fitnessmodel_class_time_fitnessmodel_days_of_week'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fitnessmodel',
            name='class_time',
        ),
    ]
