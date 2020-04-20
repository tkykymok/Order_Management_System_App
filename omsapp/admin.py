from django.contrib import admin
from .models import *



class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_code', 'name', 'address', 'phone', 'date_created')
    list_display_links = ('customer_code','name')
    list_filter = ('customer_code', )
    list_per_page = 25  
    
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier_code', 'name', 'address', 'phone', 'date_created')
    list_display_links = ('supplier_code','name')
    list_filter = ('supplier_code', )
    list_per_page = 25  

class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_code', 'parts_name', 'parts_number', 'sell_price', 'buy_price')
    list_display_links = ('item_code', 'parts_name')
    list_filter = ('item_code', )
    list_per_page = 25 

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_number','item_code', 'quantity')
    list_display_links = ('order_number',)
    list_filter = ('order_number', )
    list_per_page = 25 



admin.site.register(Customer, CustomerAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Project)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderNumber)



    
