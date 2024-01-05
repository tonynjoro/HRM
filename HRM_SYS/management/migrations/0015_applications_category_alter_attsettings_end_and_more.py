# Generated by Django 4.2.7 on 2024-01-02 21:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0014_attsettings_compassionate_leave_days_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='applications',
            name='category',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='attsettings',
            name='end',
            field=models.TimeField(default=datetime.datetime(2024, 1, 2, 21, 11, 40, 291725, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='attsettings',
            name='start',
            field=models.TimeField(default=datetime.datetime(2024, 1, 2, 21, 11, 40, 291703, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='sent',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 2, 21, 11, 40, 305261, tzinfo=datetime.timezone.utc)),
        ),
    ]