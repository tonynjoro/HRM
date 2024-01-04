# Generated by Django 4.2.7 on 2024-01-04 16:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0016_alter_applications_options_alter_approvals_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='applications',
            name='notifiers',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='department',
            name='notifiers',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='attsettings',
            name='end',
            field=models.TimeField(default=datetime.datetime(2024, 1, 4, 16, 53, 33, 187977, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='attsettings',
            name='start',
            field=models.TimeField(default=datetime.datetime(2024, 1, 4, 16, 53, 33, 187952, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='sent',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 4, 16, 53, 33, 196152, tzinfo=datetime.timezone.utc)),
        ),
    ]
