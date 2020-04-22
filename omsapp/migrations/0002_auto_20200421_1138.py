# Generated by Django 3.0.3 on 2020-04-21 02:38

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('omsapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='employee_number',
            field=models.CharField(default=57954, max_length=5, verbose_name='employee_No.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]
