# Generated by Django 5.1 on 2025-01-12 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_addressbook_is_default_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='total_orders',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customer',
            name='total_reviews',
            field=models.IntegerField(default=0),
        ),
    ]