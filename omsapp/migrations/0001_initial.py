# Generated by Django 3.0.3 on 2020-04-23 12:41

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import omsapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that employee_number  already exists.'}, max_length=5, unique=True, verbose_name='employee_number')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
                'swappable': 'AUTH_USER_MODEL',
            },
            managers=[
                ('objects', omsapp.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_code', models.CharField(max_length=5, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=30)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_code', models.CharField(max_length=5, unique=True)),
                ('parts_name', models.CharField(max_length=30)),
                ('parts_number', models.CharField(max_length=30)),
                ('sell_price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('buy_price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
                ('stock', models.IntegerField(default=0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='omsapp.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('supplier_delivery_date', models.DateField(default=datetime.datetime.today)),
                ('customer_delivery_date', models.DateField(default=datetime.datetime.today)),
                ('shipping_qty', models.IntegerField(default=0)),
                ('receiving_qty', models.IntegerField(default=0)),
                ('balance', models.IntegerField(default=0)),
                ('item_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='omsapp.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_code', models.CharField(max_length=5, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=30)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_qty', models.IntegerField(default=0)),
                ('shipped_date', models.DateField(default=datetime.datetime.today)),
                ('order_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='omsapp.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Receiving',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiving_qty', models.IntegerField(default=0)),
                ('received_date', models.DateField(default=datetime.datetime.today)),
                ('order_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='omsapp.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prj_code', models.CharField(max_length=4, unique=True)),
                ('customer_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='omsapp.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='OrderNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=8, unique=True)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='order_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='omsapp.OrderNumber'),
        ),
        migrations.AddField(
            model_name='item',
            name='prj_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='omsapp.Project'),
        ),
        migrations.AddField(
            model_name='item',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='omsapp.Supplier'),
        ),
    ]
