# Generated by Django 4.2.5 on 2023-11-16 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]