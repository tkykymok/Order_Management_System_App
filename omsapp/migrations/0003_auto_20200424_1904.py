# Generated by Django 3.0.3 on 2020-04-24 19:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('omsapp', '0002_auto_20200423_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='item',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='ordernumber',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.today),
        ),
    ]
