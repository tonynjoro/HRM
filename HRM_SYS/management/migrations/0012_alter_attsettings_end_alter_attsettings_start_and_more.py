# Generated by Django 4.2.7 on 2023-12-18 20:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0011_mailmessage_masked_sender_alter_attsettings_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attsettings',
            name='end',
            field=models.TimeField(default=datetime.datetime(2023, 12, 18, 20, 16, 9, 354463, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='attsettings',
            name='start',
            field=models.TimeField(default=datetime.datetime(2023, 12, 18, 20, 16, 9, 354431, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='sent',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 18, 20, 16, 9, 364464, tzinfo=datetime.timezone.utc)),
        ),
    ]
