# Generated by Django 5.1 on 2025-01-12 16:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_customer_total_orders_customer_total_reviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='default_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.addressbook'),
        ),
    ]
