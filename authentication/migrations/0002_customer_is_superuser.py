# Generated by Django 5.1 on 2025-01-10 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]