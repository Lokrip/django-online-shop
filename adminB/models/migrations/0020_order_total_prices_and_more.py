# Generated by Django 5.0.3 on 2024-10-24 12:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0019_alter_generatecodeconfirmationemail_expiry_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_prices',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Total Price'),
        ),
        migrations.AlterField(
            model_name='generatecodeconfirmationemail',
            name='expiry_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 24, 12, 22, 29, 996977, tzinfo=datetime.timezone.utc), verbose_name='Expiry Time'),
        ),
    ]