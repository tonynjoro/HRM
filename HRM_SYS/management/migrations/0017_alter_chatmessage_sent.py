# Generated by Django 4.2.5 on 2023-10-23 12:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0016_alter_chatmessage_sent_alter_employee_departments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='sent',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 23, 12, 1, 49, 729101, tzinfo=datetime.timezone.utc)),
        ),
    ]