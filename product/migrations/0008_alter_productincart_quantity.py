# Generated by Django 3.2.7 on 2021-09-05 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_alter_productincart_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productincart',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]