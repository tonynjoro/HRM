# Generated by Django 4.2.5 on 2023-10-24 13:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0014_alter_extrapayments_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extrapayments',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 24, 16, 47, 59, 767627)),
        ),
    ]
