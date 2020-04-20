from django.db import models
from datetime import datetime


class Customer(models.Model):
    customer_code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return str(self.customer_code +'/' + self.name)
    


class Supplier(models.Model):
    supplier_code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.name

class Project(models.Model):
    prj_code = models.CharField(max_length=4, unique=True)
    customer_code = models.ForeignKey(Customer, on_delete=models.PROTECT)
    def __str__(self):
        return self.prj_code
    

class Item(models.Model):
    item_code = models.CharField(max_length=5, unique=True)
    prj_code = models.ForeignKey(Project, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    parts_name = models.CharField(max_length=30)
    parts_number = models.CharField(max_length=30)
    sell_price = models.DecimalField(max_digits=9, decimal_places=2)
    buy_price = models.DecimalField(max_digits=9, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.item_code



class OrderNumber(models.Model):
    order_number = models.CharField(max_length=8, unique=True)
    supplier_delivery_date = models.DateField(default=datetime.today)
    customer_delivery_date = models.DateField(default=datetime.today)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.order_number
    

class Order(models.Model):
    order_number = models.ForeignKey(OrderNumber, on_delete=models.CASCADE)
    item_code = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.IntegerField()   
    def __str__(self):
        return str(self.order_number)

    

    
     
