# Generated by Django 5.0.3 on 2024-10-24 11:48

import datetime
import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0017_remove_user_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='location',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='generatecodeconfirmationemail',
            name='expiry_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 24, 11, 58, 41, 495984, tzinfo=datetime.timezone.utc), verbose_name='Expiry Time'),
        ),
    ]
