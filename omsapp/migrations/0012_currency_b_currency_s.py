# Generated by Django 3.0.3 on 2020-05-03 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('omsapp', '0011_delete_currency'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency_B',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(max_length=3, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Currency_S',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(max_length=3, unique=True)),
            ],
        ),
    ]
