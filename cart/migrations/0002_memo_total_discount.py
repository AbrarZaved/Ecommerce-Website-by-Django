# Generated by Django 5.1 on 2025-01-21 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='memo',
            name='total_discount',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
