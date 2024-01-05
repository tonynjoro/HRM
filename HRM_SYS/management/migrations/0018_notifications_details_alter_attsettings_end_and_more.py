# Generated by Django 4.2.7 on 2024-01-04 17:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0017_applications_notifiers_department_notifiers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='details',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='attsettings',
            name='end',
            field=models.TimeField(default=datetime.datetime(2024, 1, 4, 17, 9, 32, 825561, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='attsettings',
            name='start',
            field=models.TimeField(default=datetime.datetime(2024, 1, 4, 17, 9, 32, 825531, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='sent',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 4, 17, 9, 32, 835947, tzinfo=datetime.timezone.utc)),
        ),
    ]