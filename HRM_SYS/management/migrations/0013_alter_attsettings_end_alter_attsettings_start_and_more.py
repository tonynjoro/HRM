# Generated by Django 4.2.5 on 2023-11-16 04:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0012_attsettings_address_alter_attsettings_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attsettings',
            name='end',
            field=models.TimeField(default=datetime.datetime(2023, 11, 16, 4, 9, 20, 61050, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='attsettings',
            name='start',
            field=models.TimeField(default=datetime.datetime(2023, 11, 16, 4, 9, 20, 61050, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='sent',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 16, 4, 9, 20, 67033, tzinfo=datetime.timezone.utc)),
        ),
    ]
