# Generated by Django 4.1.6 on 2023-09-23 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0008_employee_attendance_alter_attendance_day_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='Attendance',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='management.attsettings'),
        ),
    ]
