# Generated by Django 4.1.6 on 2023-10-11 10:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0005_remove_applications_days_remove_applications_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='day',
            field=models.DateField(default=datetime.date(2023, 10, 11)),
        ),
        migrations.AlterField(
            model_name='employee',
            name='departments',
            field=models.CharField(choices=[('sales department', 'sales department')], default='None', max_length=50),
        ),
    ]