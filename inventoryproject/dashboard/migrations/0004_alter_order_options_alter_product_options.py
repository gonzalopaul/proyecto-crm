# Generated by Django 4.2.5 on 2023-09-28 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name_plural': 'Order'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': 'Product'},
        ),
    ]
