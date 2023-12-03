# Generated by Django 4.2.7 on 2023-11-27 19:00

import datetime
from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_approvals_template_alter_attsettings_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvals',
            name='template',
            field=tinymce.models.HTMLField(default=''),
        ),
        migrations.AlterField(
            model_name='attsettings',
            name='end',
            field=models.TimeField(default=datetime.datetime(2023, 11, 27, 19, 0, 20, 135937, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='attsettings',
            name='start',
            field=models.TimeField(default=datetime.datetime(2023, 11, 27, 19, 0, 20, 135887, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='sent',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 27, 19, 0, 20, 145246, tzinfo=datetime.timezone.utc)),
        ),
    ]