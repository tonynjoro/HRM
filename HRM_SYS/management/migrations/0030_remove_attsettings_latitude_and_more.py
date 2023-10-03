# Generated by Django 4.1.6 on 2023-10-01 15:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0009_payroll_org_name'),
        ('management', '0029_attendance_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attsettings',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='attsettings',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='attsettings',
            name='max_distance',
        ),
        migrations.RemoveField(
            model_name='attsettings',
            name='max_lat',
        ),
        migrations.RemoveField(
            model_name='attsettings',
            name='max_long',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='kra_pin',
        ),
        migrations.AddField(
            model_name='attsettings',
            name='clock_in_latitude',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='attsettings',
            name='clock_in_longitude',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='employee',
            name='payroll_settings',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='payroll.payrollsetting'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='created',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='employee',
            name='image',
            field=models.ImageField(default='emoloyee.png', upload_to='emp_images'),
        ),
    ]