# Generated by Django 4.2.5 on 2023-09-20 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0010_alter_attsettings_half_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attsettings',
            name='half_day',
        ),
    ]
