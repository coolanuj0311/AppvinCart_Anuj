# Generated by Django 5.0.1 on 2024-02-09 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_product_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='digital',
        ),
    ]