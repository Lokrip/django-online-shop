# Generated by Django 5.0.3 on 2024-10-05 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0008_productreview_email_productreview_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productreview',
            old_name='anime',
            new_name='product',
        ),
    ]
