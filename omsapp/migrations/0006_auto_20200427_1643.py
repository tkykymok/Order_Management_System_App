# Generated by Django 3.0.3 on 2020-04-27 16:43

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('omsapp', '0005_auto_20200424_1943'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acceptance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acceptance_qty', models.IntegerField(default=0)),
                ('accepted_date', models.DateField(default=datetime.datetime.today)),
                ('item_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='omsapp.Item')),
                ('order_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='omsapp.OrderNumber')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipment_qty', models.IntegerField(default=0)),
                ('shipped_date', models.DateField(default=datetime.datetime.today)),
                ('item_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='omsapp.Item')),
                ('order_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='omsapp.OrderNumber')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='shipping',
            name='item_code',
        ),
        migrations.RemoveField(
            model_name='shipping',
            name='order_number',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='receiving_qty',
            new_name='acceptance_qty',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='shipping_qty',
            new_name='shipment_qty',
        ),
        migrations.DeleteModel(
            name='Receiving',
        ),
        migrations.DeleteModel(
            name='Shipping',
        ),
    ]
