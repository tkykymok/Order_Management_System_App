from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _



class CustomUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('username','password')}),
        (_('Personal info'), {'fields': ('last_name','first_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'last_name', 'first_name', 'is_staff')
    search_fields = ('username', 'full_name')


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
    list_display = ('item_code', 'parts_name', 'parts_number', 'sell_price', 'buy_price', 'supplier')
    list_display_links = ('item_code', 'parts_name')
    list_filter = ('item_code', )
    list_per_page = 25 

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_number','supplier_delivery_date','customer_delivery_date','item_code', 'quantity','balance')
    list_display_links = ('order_number',)
    list_filter = ('order_number', )
    list_per_page = 25 
    
class OrderNumberAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_number', 'date_created', 'user')
    list_display_links = ('order_number',)
    list_filter = ('order_number', )
    list_per_page = 25 
    


admin.site.register(User, CustomUserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Project)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderNumber, OrderNumberAdmin)
admin.site.register(Shipping)
admin.site.register(Receiving)


    
