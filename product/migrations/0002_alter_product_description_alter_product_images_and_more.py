# Generated by Django 5.1 on 2025-01-10 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_details',
            field=models.TextField(),
        ),
    ]