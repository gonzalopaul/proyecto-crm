# Generated by Django 4.2.5 on 2023-09-27 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Vapes con Nic', 'Vapes con Nic'), ('Vapes sin Nic', 'Vapes sin Nic'), ('Vapes 600 puffs', 'Vapes 600 puffs')], max_length=20, null=True),
        ),
    ]
