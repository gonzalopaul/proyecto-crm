# Generated by Django 4.2.5 on 2023-11-23 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_order_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='iva_rate',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]
