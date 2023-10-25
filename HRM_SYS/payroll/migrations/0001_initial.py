# Generated by Django 4.2.5 on 2023-10-25 09:07

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraPayments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=100)),
                ('overtime_hours', models.FloatField(default=0.0)),
                ('overtime_rate', models.FloatField(default=0.0)),
                ('incentive', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('performance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('awards', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('loan_deductions', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('welfare_deductions', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created', models.DateTimeField(default=datetime.datetime(2023, 10, 25, 12, 7, 17, 411856))),
            ],
        ),
        migrations.CreateModel(
            name='PayRoll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_name', models.CharField(max_length=100, null=True)),
                ('payroll_id', models.CharField(max_length=100, null=True)),
                ('employee_id', models.CharField(max_length=100, null=True)),
                ('sign_id', models.CharField(max_length=100, null=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('id_no', models.CharField(max_length=100, null=True)),
                ('pin_no', models.CharField(max_length=100, null=True)),
                ('phone', models.CharField(max_length=100, null=True)),
                ('role', models.CharField(max_length=100, null=True)),
                ('account_no', models.CharField(max_length=100, null=True)),
                ('basic_salary', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('allowance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('add_ons', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total_days', models.FloatField(default=0.0)),
                ('overtime_hours', models.FloatField(default=0.0)),
                ('overtime_pay', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('incentives', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('leave_days', models.FloatField(default=0.0)),
                ('deductions', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('gross_pay', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('taxable_income', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('tax', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('nhif', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('nssf', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('insurance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('housing', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('loan_deductions', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('welfare_deductions', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('others', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('net_pay', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_date', models.DateField(default=django.utils.timezone.now)),
                ('created_time', models.TimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(default='audit', max_length=100)),
                ('pay_run', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PayRollSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_name', models.CharField(default='', max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('tax_rate', models.TextField(default='24000=10%,8333=25%,467667=30%,300000=32.5%')),
                ('relief', models.DecimalField(decimal_places=2, default=2400.0, max_digits=10)),
                ('nssf', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('nhif', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('health_insurance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('housing', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('others', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
    ]
