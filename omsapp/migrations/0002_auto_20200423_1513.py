# Generated by Django 3.0.3 on 2020-04-23 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('omsapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiving',
            name='item_code',
            field=models.ForeignKey(default=10000, on_delete=django.db.models.deletion.CASCADE, to='omsapp.Item'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shipping',
            name='item_code',
            field=models.ForeignKey(default=10000, on_delete=django.db.models.deletion.CASCADE, to='omsapp.Item'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='receiving',
            name='order_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='omsapp.OrderNumber'),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='order_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='omsapp.OrderNumber'),
        ),
    ]
