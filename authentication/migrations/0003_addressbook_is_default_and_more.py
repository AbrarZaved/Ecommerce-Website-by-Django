# Generated by Django 5.1 on 2025-01-12 10:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_customer_default_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressbook',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customer',
            name='default_address',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.addressbook'),
        ),
    ]
