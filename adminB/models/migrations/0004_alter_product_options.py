# Generated by Django 5.0.3 on 2024-09-29 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0003_brand_categories_colormodel_order_product_orderitem_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
    ]