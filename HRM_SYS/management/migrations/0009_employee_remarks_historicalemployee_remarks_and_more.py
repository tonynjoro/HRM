# Generated by Django 4.2.5 on 2023-11-14 04:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0008_alter_approvals_name_alter_attsettings_end_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='remarks',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='historicalemployee',
            name='remarks',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='attsettings',
            name='end',
            field=models.TimeField(default=datetime.datetime(2023, 11, 14, 4, 50, 34, 763959, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='attsettings',
            name='start',
            field=models.TimeField(default=datetime.datetime(2023, 11, 14, 4, 50, 34, 763959, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='sent',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 14, 4, 50, 34, 769949, tzinfo=datetime.timezone.utc)),
        ),
    ]
