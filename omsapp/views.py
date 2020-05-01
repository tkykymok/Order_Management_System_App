from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import (
    View,
    ListView,
    DetailView,
    UpdateView
)
from omsapp.models import Order, Item, OrderNumber, Order, Project, User, Shipment, Acceptance
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
# from extra_views import InlineFormSetFactory, CreateWithInlinesView, UpdateWithInlinesView
from django.views.generic import TemplateView
from .forms import OrderNumberForm, OrderForm

from django.http import JsonResponse
from django.forms.models import model_to_dict

import pandas as pd
from django_pandas.io import read_frame

import json


class MenuView(View,LoginRequiredMixin):
    def get(self, request):
        return render(request, 'omsapp/menu.html')

### Order ########################### 
class OrderEntryView(View, LoginRequiredMixin):
    def get(self,request):
        user = request.user
        context = {'user':user}
        return render(request, 'omsapp/order_entry.html')

class PrjCodeGet(View, LoginRequiredMixin):
    def post(self, request):
        prj_code_get = request.POST.getlist('prjCode', None)
        prj_code = Project.objects.get(prj_code = prj_code_get[0])
        customer_info = prj_code.customer_code
        person_incharge = request.user
        return JsonResponse({'customer_info':model_to_dict(customer_info), 'person_incharge':model_to_dict(person_incharge)}, status=200)
    
class OrderNumberCreate(View, LoginRequiredMixin):
    def post(self, request):
        user = request.user
        order_number = request.POST.get('orderNumber',None)
        new_order_number = OrderNumber(
            user = user,
            order_number=order_number)
        if order_number == "":
            return redirect ('order_entry')
        else:
            new_order_number.save()
        
        return JsonResponse({'orderNumber':model_to_dict(new_order_number)}, status=200)
        
class ItemInfoGet(View, LoginRequiredMixin):
    def post(self, request):
        item_code = request.POST.get('item', None)
        item_info = Item.objects.get(item_code=item_code)
        prj = item_info.prj_code.prj_code
        # return JsonResponse({'result':True}, status=200)
        return JsonResponse({'item_info':model_to_dict(item_info),'prj':prj}, status=200)
    
    
class OrderCreateConfirm(View, LoginRequiredMixin):
    def post(self, request):
        input_order_number = request.POST.get('orderNumber', None)
    
        items = request.POST.getlist('item', None)
        qtys = request.POST.getlist('qty', None)
        suppDates = request.POST.getlist('suppDate', None)
        custDates = request.POST.getlist('custDate', None)
                
        for i in range(len(items)):
            if items[i] == "":
                break
            else:      
                Order.objects.create(
                    order_number = OrderNumber.objects.get(order_number=input_order_number),
                    item_code = Item.objects.get(item_code = items[i]),
                    quantity = qtys[i],
                    supplier_delivery_date = suppDates[i],
                    customer_delivery_date = custDates[i],
                    balance = qtys[i]
                )
        return JsonResponse({'result':True}, status=200)

class OrderUpdateDataGet(View):
    def post(self, request):
        input_order_number = request.POST.get('orderNumber', None)
        order_number = OrderNumber.objects.get(order_number=input_order_number)
        
        rf_order = read_frame(Order.objects.filter(order_number=order_number).order_by('id'))
        
        rf_item = read_frame(Item.objects.all(),fieldnames=[
            'item_code',
            'parts_name', 
            'parts_number', 
            'sell_price',
            'buy_price'
        ])
        
        data1 = pd.merge(rf_order, rf_item, on='item_code', how='left')
        
        data2 = data1.to_dict()
    
        return JsonResponse({'order_list':data2}, status=200)
    
class OrderUpdateConfirm(View):
    def post(self, request):
        input_order_number = request.POST.get('orderNumber', None)
        order_id = request.POST.getlist('orderId', None)
        items = request.POST.getlist('item', None)
        qtys = request.POST.getlist('qty', None)
        suppDates = request.POST.getlist('suppDate', None)
        custDates = request.POST.getlist('custDate', None)
        
        for i in range(len(order_id)):
            update_order = Order.objects.get(id=order_id[i])
            update_order.supplier_delivery_date = suppDates[i]
            update_order.customer_delivery_date = custDates[i]
            update_order.save()
            
        return JsonResponse({'result':True}, status=200)
                
        
        
class OrderDeleteConfirm(View):
    def post(self, request):
        delete_check = request.POST.getlist('deleteCheckNum', None)
        order_id = request.POST.getlist('orderId', None)
        
        for i in range(len(order_id)):
            if delete_check[i] == "1":
                Order.objects.get(id=order_id[i]).delete()
            else:
                pass
    
        return JsonResponse({'result':True}, status=200)


### Shipment ########################### 
class ShipmentEntryView(View):
    def get(self, request):
        user = request.user
        context = {'user':user}
        return render(request, 'omsapp/shipment_entry.html', context)
    
class ShipmentDataGet(View):
    def get(self, request):
        input_order_number = request.GET.get('shipOrderNumber', None)
        parent_order_number = OrderNumber.objects.get(order_number = input_order_number)
        
        rf_ship_order = read_frame(Order.objects.filter(order_number=parent_order_number).order_by('id'))
        rf_item = read_frame(Item.objects.all(),fieldnames=[
            'item_code',
            'prj_code',
            'customer',
            'parts_name', 
            'parts_number', 
            'sell_price',
            'buy_price'
        ])
        
        data1 = pd.merge(rf_ship_order, rf_item, on='item_code', how='left')        
        data2 = data1.to_dict()
    
        return JsonResponse({'ship_order_list':data2}, status=200)

class ShipmentComplete(View):
    def post(self, request):
        order_id = request.POST.getlist('orderId', None)
        item_code_list = request.POST.getlist('shipItem', None)
        ship_date_list = request.POST.getlist('shipDate2', None)
        ship_qty_list = request.POST.getlist('shipQty', None)
        
        for i in range(len(ship_qty_list)):
            if ship_qty_list[i] == "":
                break
            else:      
                Shipment.objects.create(
                    user = request.user,
                    order_number = Order.objects.get(id=order_id[i]),
                    item_code = Item.objects.get(item_code=item_code_list[i]),
                    shipped_date = ship_date_list[i],
                    shipment_qty = int(ship_qty_list[i]),
                )
                
        for i in range(len(order_id)):
            order_data = Order.objects.get(id=int(order_id[i]))
            if ship_qty_list[i] == '':
                pass
            else:
                order_data.shipment_qty += int(ship_qty_list[i])
                order_data.stock -= int(ship_qty_list[i])
                order_data.save()
        
        return JsonResponse({'result':True}, status=200)
    
class ShipmentUpdateDataGet(View):
    def get(self, request):
        input_order_number = request.GET.get('shipOrderNumber', None)
        input_id = request.GET.get('orderId', None)
        order = Order.objects.get(id=input_id)
                
        rf_ship_order = read_frame(Shipment.objects.filter(order_number=order).order_by('id'))
        
        rf_order = read_frame(Order.objects.filter(id=input_id),fieldnames=[
            'id',
            'order_number'
        ])
        
        rf_item = read_frame(Item.objects.all(),fieldnames=[
            'item_code',
            'prj_code',
            'customer',
            'parts_name', 
            'parts_number', 
            'sell_price',
            'buy_price'
        ])
  
        data1 = pd.merge(rf_ship_order, rf_item, on='item_code', how='left')
        data2 = pd.merge(data1, rf_order, on='order_number', how='inner')
        
        data3 = data2.to_dict()
        return JsonResponse({'shipment_list':data3}, status=200)
        

class ShipmentUpdateConfirm(View):
    def post(self,request):
        orderId_list = request.POST.getlist('orderId', None)
        ship_date_list = request.POST.getlist('shipDate2', None)
        shipId_list = request.POST.getlist('shipId', None)
        qty_list = request.POST.getlist('shipQty', None)
                
        for i in range (len(shipId_list)):
            parent_order = Order.objects.get(id=orderId_list[i])
            data = Shipment.objects.get(id=shipId_list[i])
            changed_ship_date = ship_date_list[i]
            original_qty = data.shipment_qty
            changed_qty = int(qty_list[i])
            if original_qty == changed_qty:
                pass
            else:
                data.shipped_date = changed_ship_date
                data.shipment_qty = changed_qty
                data.save()
                parent_order.shipment_qty -= int(original_qty)
                parent_order.shipment_qty += int(changed_qty)
                parent_order.stock += int(original_qty)
                parent_order.stock -= int(changed_qty)
                parent_order.save()
            
        
        return JsonResponse({'result':True}, status=200)

class ShipmentDeleteConfirm(View):
    def post(self, request):
        delete_check = request.POST.getlist('deleteCheckNum', None)
        orderId_list = request.POST.getlist('orderId', None)
        shipId_list = request.POST.getlist('shipId', None)
          
        for i in range (len(shipId_list)):
            if delete_check[i] == "1":
                parent_order = Order.objects.get(id=orderId_list[i])
                data = Shipment.objects.get(id=shipId_list[i])
                original_qty = data.shipment_qty
                parent_order.shipment_qty -= int(original_qty)
                parent_order.stock += int(original_qty)
                parent_order.save()
                data.delete()
            else:
                pass
            
        return JsonResponse({'result':True}, status=200)
    


### Acceptance ########################### 
class AcceptanceEntryView(View):
    def get(self, request):
        user = request.user
        context = {'user':user}
        return render(request, 'omsapp/acceptance_entry.html', context)
    
class AcceptanceDataGet(View):
    def get(self, request):
        input_order_number = request.GET.get('acceptOrderNumber', None)
        supplier_code = request.GET.get('supplier', None)
        parent_order_number = OrderNumber.objects.get(order_number = input_order_number)
        
        rf_accept_order = read_frame(Order.objects.filter(order_number=parent_order_number).order_by('id'))
        
        rf_item = read_frame(Item.objects.all(),fieldnames=[
            'item_code',
            'prj_code',
            'supplier',
            'parts_name', 
            'parts_number', 
            'sell_price',
            'buy_price'
        ])
        
        data1 = pd.merge(rf_accept_order, rf_item, on='item_code', how='left')
        
        data2 = data1.to_dict()
    
        return JsonResponse({'accept_order_list':data2}, status=200)
      
class AcceptanceComplete(View):
    def post(self, request):
        input_order_number = request.POST.get('orderNumber', None)
        order_id = request.POST.getlist('orderId', None)
        item_code_list = request.POST.getlist('acceptItem', None)
        accept_date_list = request.POST.getlist('acceptDate2', None)
        accept_qty_list = request.POST.getlist('acceptQty', None)
        
        for i in range(len(accept_qty_list)):
            if accept_qty_list[i] == "":
                break
            else:      
                Acceptance.objects.create(
                    user = request.user,
                    order_number = Order.objects.get(id=order_id[i]),
                    item_code = Item.objects.get(item_code=item_code_list[i]),
                    accepted_date = accept_date_list[i],
                    acceptance_qty = int(accept_qty_list[i]),
                )
                
        for i in range(len(order_id)):
            order_data = Order.objects.get(id=int(order_id[i]))
            if accept_qty_list[i] == '':
                pass
            else:
                order_data.acceptance_qty += int(accept_qty_list[i])
                order_data.stock += int(accept_qty_list[i])
                order_data.balance -= int(accept_qty_list[i])
                order_data.save()
        
        return JsonResponse({'result':True}, status=200)
    

class AcceptanceUpdateDataGet(View):
    def get(self, request):
        input_order_number = request.GET.get('shipOrderNumber', None)
        input_id = request.GET.get('orderId', None)
        order = Order.objects.get(id=input_id)

        rf_accept_order = read_frame(Acceptance.objects.filter(order_number=order).order_by('id'))
        
        rf_order = read_frame(Order.objects.filter(id=input_id),fieldnames=[
            'id',
            'order_number',
            'balance',
            'stock'
            
        ])
        rf_item = read_frame(Item.objects.all(),fieldnames=[
            'item_code',
            'prj_code',
            'supplier',
            'parts_name', 
            'parts_number', 
            'sell_price',
            'buy_price'
        ])
  
        data1 = pd.merge(rf_accept_order, rf_item, on='item_code', how='left')
        data2 = pd.merge(data1, rf_order, on='order_number', how='inner')
        data3 = data2.to_dict()
        return JsonResponse({'acceptance_list':data3}, status=200)
   

class AcceptanceUpdateConfirm(View):
    def post(self,request):
        orderId_list = request.POST.getlist('orderId', None)
        accept_date_list = request.POST.getlist('acceptDate2', None)
        acceptId_list = request.POST.getlist('acceptId', None)
        qty_list = request.POST.getlist('acceptQty', None)
                
        for i in range (len(acceptId_list)):
            parent_order = Order.objects.get(id=orderId_list[i])
            data = Acceptance.objects.get(id=acceptId_list[i])
            changed_accept_date = accept_date_list[i]
            original_qty = data.acceptance_qty
            changed_qty = int(qty_list[i])
            data.accepted_date = changed_accept_date
            data.acceptance_qty = changed_qty
            data.save()
            parent_order.acceptance_qty -= int(original_qty)
            parent_order.acceptance_qty += int(changed_qty)
            parent_order.stock -= int(original_qty)
            parent_order.stock += int(changed_qty)
            parent_order.balance += int(original_qty)
            parent_order.balance -= int(changed_qty)
            parent_order.save()

        return JsonResponse({'result':True}, status=200)

class AcceptanceDeleteConfirm(View):
    def post(self, request):
        delete_check = request.POST.getlist('deleteCheckNum', None)
        orderId_list = request.POST.getlist('orderId', None)
        acceptId_list = request.POST.getlist('acceptId', None)
        
        for i in range (len(acceptId_list)):
            if delete_check[i] == "1":
                parent_order = Order.objects.get(id=orderId_list[i])
                data = Acceptance.objects.get(id=acceptId_list[i])
                original_qty = data.acceptance_qty
                parent_order.acceptance_qty -= int(original_qty)
                parent_order.balance += int(original_qty)
                parent_order.stock -= int(original_qty)
                parent_order.save()
                data.delete()
            else:
                pass
        return JsonResponse({'result':True}, status=200)

    
### Order Info ########################### 
class OrderInfoView(View, LoginRequiredMixin):
    def get(self, request):   
        input_prj_code = request.GET.get('prjCode', None)
        input_order_number = request.GET.get('orderNum', None)
        input_order_date_s = request.GET.get('orderDateS', None)
        input_order_date_e = request.GET.get('orderDateE', None)    
    
       
        rf_order = read_frame(Order.objects.all().order_by('id'))
     
        rf_item = read_frame(Item.objects.all(),fieldnames=[
            'item_code',
            'prj_code', 
            'customer', 
            'supplier', 
            'parts_name', 
            'parts_number', 
            'sell_price','buy_price'
        ])
        
        data1 = pd.merge(rf_order, rf_item, on='item_code', how='inner')
        
        rf_order_number = read_frame(OrderNumber.objects.all(), fieldnames=[
            'order_number',
            'user',
            'date_created'
        ])
        
        data2 = pd.merge(
            data1.sort_values('id'), 
            rf_order_number, 
            on='order_number', 
            how='inner'
            )
 

        # 1. prj_code only
        if input_prj_code != "" and input_order_number == "" and input_order_date_s == "" and input_order_date_e == "":
            order_list = data2[data2['prj_code']==input_prj_code]
            context = {
                'order_list':order_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'order_date_s':input_order_date_s,
                'order_date_e':input_order_date_e}
            print('1')
            return render(request, 'omsapp/order_info.html',context)
            
        # 2. Order_No. only
        elif input_prj_code == "" and input_order_number != "" and input_order_date_s == "" and input_order_date_e == "":
            order_list = data2[data2['order_number']==input_order_number]
            context = {
                'order_list':order_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'order_date_s':input_order_date_s,
                'order_date_e':input_order_date_e}
            print('2')
            return render(request, 'omsapp/order_info.html',context)
            
        # 3. order_date_s only
        elif input_prj_code == "" and input_order_number == "" and input_order_date_s != "" and input_order_date_e == "":
            order_date_s = pd.to_datetime(input_order_date_s).floor('D')
            order_list = data2[data2['date_created']>=order_date_s]         
            context = {
                'order_list':order_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'order_date_s':input_order_date_s,
                'order_date_e':input_order_date_e}
            print('3')
            return render(request, 'omsapp/order_info.html',context)
            
        # 4. order_date_e only
        elif input_prj_code == "" and input_order_number == "" and input_order_date_s == "" and input_order_date_e != "":
            order_list = data2[data2['date_created']<=order_date_e]
            context = {
                'order_list':order_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'order_date_s':input_order_date_s,
                'order_date_e':input_order_date_e}
            print('4')
            return render(request, 'omsapp/order_info.html',context) 
            
        # 5. order_date_s and order_date_e
        elif input_prj_code == "" and input_order_number == "" and input_order_date_s != "" and input_order_date_e != "":
            order_date_s = pd.to_datetime(input_order_date_s).floor('D')
            order_date_e = pd.to_datetime(input_order_date_e).floor('D')
            data3 = data2[data2['date_created']>=order_date_s]
            order_list = data3[data3['date_created']<=order_date_e]
            context = {
                'order_list':order_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'order_date_s':input_order_date_s,
                'order_date_e':input_order_date_e}
            print('5')
            return render(request, 'omsapp/order_info.html',context)
        
        # 6. prj_code and Order_No
        elif input_prj_code != "" and input_order_number != "" and input_order_date_s == "" and input_order_date_e == "":
            data3 = data2[data2['prj_code']==input_prj_code]
            order_list = data3[data3['order_number']==input_order_number]
            context = {
                'order_list':order_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'order_date_s':input_order_date_s,
                'order_date_e':input_order_date_e}      
            print('6')      
            return render(request, 'omsapp/order_info.html',context)
        
        # 7. prj_code and order_date_s
        elif input_prj_code != "" and input_order_number == "" and input_order_date_s != "" and input_order_date_e == "":
            order_date_s = pd.to_datetime(input_order_date_s).floor('D')
            data3 = data2[data2['prj_code']==input_prj_code]
            order_list = data3[data3['date_created']>=order_date_s]
            context = {
                'order_list':order_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'order_date_s':input_order_date_s,
                'order_date_e':input_order_date_e}
            print('7')
            return render(request, 'omsapp/order_info.html',context)
            
        # 8. prj_code and order_date_s and order_date_e
        elif input_prj_code != "" and input_order_number == "" and input_order_date_s != "" and input_order_date_e != "":
            order_date_s = pd.to_datetime(input_order_date_s).floor('D')
            order_date_e = pd.to_datetime(input_order_date_e).floor('D')
            data3 = data2[data2['prj_code']==input_prj_code]
            data4 = data3[data3['date_created']>=order_date_s]
            order_list = data4[data4['date_created']<=order_date_e]
            context = {
                'order_list':order_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'order_date_s':input_order_date_s,
                'order_date_e':input_order_date_e}
            print('8')
            return render(request, 'omsapp/order_info.html',context)
        
        # 9. Order_No and order_date_s
        elif input_prj_code == "" and input_order_number != "" and input_order_date_s != "" and input_order_date_e == "":
            order_date_s = pd.to_datetime(input_order_date_s).floor('D')
            data3 = data2[data2['order_number']==input_order_number]
            order_list = data3[data3['date_created']>=order_date_s]
            context = {
                'order_list':order_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'order_date_s':input_order_date_s,
                'order_date_e':input_order_date_e}
            print('9')
            return render(request, 'omsapp/order_info.html',context)
        
        # 10. Order_No and order_date_s and order_date_e
        elif input_prj_code == "" and input_order_number != "" and input_order_date_s != "" and input_order_date_e != "":
            order_date_s = pd.to_datetime(input_order_date_s).floor('D')
            order_date_e = pd.to_datetime(input_order_date_e).floor('D')
            data3 = data2[data2['order_number']==input_order_number]
            data4 = data3[data3['date_created']>=order_date_s]
            order_list = data4[data4['date_created']<=order_date_e]
            context = {
                'order_list':order_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'order_date_s':input_order_date_s,
                'order_date_e':input_order_date_e}
            print('10')
            return render(request, 'omsapp/order_info.html',context)
        
        # 11. No input
        elif input_prj_code == "" and input_order_number == "" and input_order_date_s == "" and input_order_date_e == "":
            order_list = data2 
            context = {
                'order_list':order_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'order_date_s':input_order_date_s,
                'order_date_e':input_order_date_e}
            print('11')
            return render(request, 'omsapp/order_info.html',context)
        
        # 12. default
        elif input_prj_code is None and input_order_number is None and input_order_date_s is None and input_order_date_e is None:
            print('12')            
            return render(request, 'omsapp/order_info.html')
        
        # 13. All Input 
        else:
            order_date_s = pd.to_datetime(input_order_date_s).floor('D')
            order_date_e = pd.to_datetime(input_order_date_e).floor('D')
            data3 = data2[data2['prj_code']==input_prj_code]
            data4 = data3[data3['order_number']==input_order_number]
            data5 = data4[data4['date_created']>=order_date_s]
            order_list = data5[data5['date_created']<=order_date_e]
            context = {
                'order_list':order_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'order_date_s':input_order_date_s,
                'order_date_e':input_order_date_e}
            print('13')
            return render(request, 'omsapp/order_info.html',context)
            