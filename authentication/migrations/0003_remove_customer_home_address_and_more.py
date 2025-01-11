# Generated by Django 5.1 on 2025-01-11 16:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_customer_is_superuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='home_address',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='office_address',
        ),
        migrations.CreateModel(
            name='Addressbook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('zone', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('address_label', models.CharField(choices=[('home', 'Home'), ('office', 'Office')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
