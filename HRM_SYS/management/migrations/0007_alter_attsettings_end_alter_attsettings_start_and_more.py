# Generated by Django 4.2.5 on 2023-12-07 05:53

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_alter_attsettings_end_alter_attsettings_start_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attsettings',
            name='end',
            field=models.TimeField(default=datetime.datetime(2023, 12, 7, 5, 53, 52, 76077, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='attsettings',
            name='start',
            field=models.TimeField(default=datetime.datetime(2023, 12, 7, 5, 53, 52, 76077, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='sent',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 7, 5, 53, 52, 81906, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='MailMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mail_recipient', to='management.profile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mail_sender', to='management.profile')),
            ],
        ),
    ]