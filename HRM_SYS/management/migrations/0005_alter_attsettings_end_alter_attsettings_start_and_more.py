# Generated by Django 4.2.5 on 2023-11-29 04:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_alter_approvals_template_alter_attsettings_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attsettings',
            name='end',
            field=models.TimeField(default=datetime.datetime(2023, 11, 29, 4, 34, 38, 836342, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='attsettings',
            name='start',
            field=models.TimeField(default=datetime.datetime(2023, 11, 29, 4, 34, 38, 836342, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='sent',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 29, 4, 34, 38, 841377, tzinfo=datetime.timezone.utc)),
        ),
    ]