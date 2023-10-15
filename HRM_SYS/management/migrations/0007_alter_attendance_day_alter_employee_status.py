# Generated by Django 4.1.6 on 2023-10-14 07:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_alter_attendance_day_alter_employee_departments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='day',
            field=models.DateField(default=datetime.date(2023, 10, 14)),
        ),
        migrations.AlterField(
            model_name='employee',
            name='status',
            field=models.CharField(choices=[('incomplete', 'incomplete'), ('active', 'active'), ('resigned', 'resigned'), ('suspended', 'suspended')], default='None', max_length=50),
        ),
    ]