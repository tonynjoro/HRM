# Generated by Django 4.1.6 on 2023-10-01 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0027_attendance_days_attsettings_expected_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='attsettings',
            name='max_distance',
            field=models.FloatField(default=100.0),
        ),
        migrations.AddField(
            model_name='attsettings',
            name='max_lat',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='attsettings',
            name='max_long',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='employee',
            name='image',
            field=models.ImageField(default='employee.png', upload_to='emp_images'),
        ),
    ]