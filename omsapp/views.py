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

    
class OrderEntryView(View, LoginRequiredMixin):
    def get(self,request):
        user = request.user
        context = {'user':user}
        return render(request, 'omsapp/order_entry.html')

class PrjCodeGet(View, LoginRequiredMixin):
    def post(self, request):
        prj_code_get = request.POST.getlist('prjCode', None)
        print(prj_code_get)
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

class OrderUpdateInfo(View):
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
        
        data1 = pd.merge(rf_order, rf_item, on='item_code', how='inner')
        
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
            if update_order.shipment_qty == 0 and update_order.acceptance_qty == 0:
                print(update_order.shipment_qty)
                update_order.supplier_delivery_date = suppDates[i]
                update_order.customer_delivery_date = custDates[i]
                update_order.quantity = int(qtys[i])
                update_order.balance = int(qtys[i])
                update_order.save()
            else:
                pass
                
        
        return JsonResponse({'result':True}, status=200)
        
        

        
class OrderDeleteConfirm(View):
    def post(self, request):
        order_id = request.POST.getlist('orderId', None)
        for i in range(len(order_id)):
            Order.objects.get(id=order_id[i]).delete()
    
        return JsonResponse({'result':True}, status=200)



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
        print(data2)

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
            print(type(order_list.values) )
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
        
        # 13. default
        elif input_prj_code is None and input_order_number is None and input_order_date_s is None and input_order_date_e is None:
            print('13')
            print(input_prj_code)
            print(input_order_number)
            print(input_order_date_s)
            print(input_order_date_e)
            
            return render(request, 'omsapp/order_info.html')
        
        # 12. All Input 
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
            print('12')
            return render(request, 'omsapp/order_info.html',context)
            

    # def post(self, request):
    #     get_id = request.POST.get('formId', None)
    #     new_supp_del_date = request.POST.get('suppDelDate', None)
    #     new_cust_del_date = request.POST.get('custDelDate', None)
    #     new_qty = request.POST.get('qty', None)
                
    #     new_order = Order.objects.get(id=get_id)
    #     new_order.quantity = int(new_qty)
    #     new_order.supplier_delivery_date = new_supp_del_date
    #     new_order.customer_delivery_date = new_cust_del_date 
    #     new_order.save()        
            
    #     return JsonResponse({'new_order':model_to_dict(new_order)}, status=200)  


class ShipmentEntryView(View):
    def get(self, request):
        user = request.user
        context = {'user':user}
        return render(request, 'omsapp/shipment_entry.html', context)
    
class ShipmentDataGet(View):
    def get(self, request):
        input_order_number = request.GET.get('shipOrderNumber', None)
        parent_order_number = OrderNumber.objects.get(order_number = input_order_number)
        order_set = Order.objects.filter(order_number=parent_order_number)
        pic = request.user
        order_data = []
        item_codes = []
        item_data = []
        
        for i in order_set:
            order_data.append(model_to_dict(i))
            item_codes.append(i.item_code)
        for i in item_codes:
            item_data.append(model_to_dict(i))
        
        prj_code = item_codes[0].prj_code
        customer = item_codes[0].prj_code.customer_code
        
        return JsonResponse({
            'order_data':order_data,
            'item_data':item_data,
            'pic':model_to_dict(pic),
            'prj_code':model_to_dict(prj_code),
            'customer':model_to_dict(customer)
            }, status=200)

class ShipmentComplete(View):
    def post(self, request):
        input_order_number = request.POST.get('orderNumber', None)
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
                    order_number = OrderNumber.objects.get(order_number=input_order_number),
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
                # order_data.balance -= int(ship_qty_list[i])
                order_data.save()
        
        return JsonResponse({'result':True}, status=200)


