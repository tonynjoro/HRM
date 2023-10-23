# Generated by Django 4.2.5 on 2023-10-18 09:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0005_alter_payroll_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payroll',
            name='created',
        ),
        migrations.AddField(
            model_name='payroll',
            name='created_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='payroll',
            name='created_time',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]