# Generated by Django 5.2.2 on 2025-06-08 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_alter_fitnessmodel_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitnessmodel',
            name='days_of_week',
            field=models.JSONField(default=list),
        ),
    ]
