# Generated by Django 5.1 on 2025-01-26 11:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_memo_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('memo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.memo')),
            ],
        ),
    ]
