# Generated by Django 5.0.3 on 2024-11-04 09:52

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0022_remove_checkoutmodel_shipping_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatecodeconfirmationemail',
            name='expiry_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 4, 10, 2, 4, 957310, tzinfo=datetime.timezone.utc), verbose_name='Expiry Time'),
        ),
        migrations.AlterField(
            model_name='productimagemodel',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='models.product', verbose_name='Product'),
        ),
    ]