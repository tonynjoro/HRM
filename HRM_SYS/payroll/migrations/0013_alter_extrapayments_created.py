# Generated by Django 4.2.5 on 2023-10-24 08:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0012_payroll_loan_deductions_payroll_welfare_deductions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extrapayments',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
