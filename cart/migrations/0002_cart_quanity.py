# Generated by Django 5.1 on 2025-01-13 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quanity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
