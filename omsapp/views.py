from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import (
    View,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from omsapp.models import Order, Item, OrderNumber, Order, Project, User, Shipment, Acceptance, Customer, Supplier, Currency_S, Currency_B, Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .forms import CustomerCreateForm, SupplierCreateForm, ProjectCreateForm, TaskForm
from datetime import datetime

from django.http import JsonResponse
from django.forms.models import model_to_dict

from django.utils.decorators import method_decorator
from omsapp.decorators import admin_only

import pandas as pd
from django_pandas.io import read_frame

import json
from io import BytesIO 
from StyleFrame import StyleFrame

### Login ########################### 
class Login(LoginView):
    template_name = 'registration/login.html'



### Menu & ToDo ########################### 
class MenuView(LoginRequiredMixin, View):
    def get(self, request):
        user = User.objects.get(username=request.user)
        initial_dict = {'user':user}
        form = TaskForm(initial=initial_dict)
        tasks = Task.objects.filter(user=user).order_by('-id')
        context = {'form':form, 'tasks':tasks}
        
        return render(request, 'omsapp/menu.html', context)
    
    def post(self, request):
        user = User.objects.get(username=request.user)
        initial_dict = {'user':user}
        form = TaskForm(request.POST, initial=initial_dict)
        
        if form.is_valid():
            new_task = form.save()
            return JsonResponse({'task':model_to_dict(new_task)}, status=200)
        else:
            return redirect ('menu')
        
class TaskComplete(View):
    def post(self, request, id):
        task = Task.objects.get(id=id)
        task.completed  = True
        task.save()
        return JsonResponse({'task':model_to_dict(task)}, status=200)
        
class TaskDelete(View):
    def post(self,request, id):
        delete_task = Task.objects.get(id=id)
        delete_task.delete()
        return JsonResponse({'result':True}, status=200)

### Order ########################### 
class OrderEntryView(LoginRequiredMixin,View):
    def get(self,request):
        user = request.user
        context = {'user':user}
        return render(request, 'omsapp/order_entry.html')

class PrjCodeGet(LoginRequiredMixin,View):
    def post(self, request):
        prj_code_get = request.POST.getlist('prjCode', None)
        prj_code = Project.objects.get(prj_code = prj_code_get[0])
        customer_info = prj_code.customer
        person_incharge = request.user
        return JsonResponse({'customer_info':model_to_dict(customer_info), 'person_incharge':model_to_dict(person_incharge)}, status=200)
    
class OrderNumberCreate(LoginRequiredMixin,View):
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
        
class ItemInfoGet(LoginRequiredMixin,View):
    def post(self, request):
        item_code = request.POST.get('item', None)
        item_info = Item.objects.get(item_code=item_code)
        prj = item_info.prj_code.prj_code
        # return JsonResponse({'result':True}, status=200)
        return JsonResponse({'item_info':model_to_dict(item_info),'prj':prj}, status=200)
    
    
class OrderCreateConfirm(LoginRequiredMixin,View):
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

class OrderUpdateDataGet(LoginRequiredMixin,View):
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
    
class OrderUpdateConfirm(LoginRequiredMixin,View):
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
                
        
        
class OrderDeleteConfirm(LoginRequiredMixin,View):
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
class ShipmentEntryView(LoginRequiredMixin,View):
    def get(self, request):
        user = request.user
        context = {'user':user}
        return render(request, 'omsapp/shipment_entry.html', context)
    
class ShipmentDataGet(LoginRequiredMixin,View):
    def get(self, request):
        input_order_number = request.GET.get('shipOrderNumber', None)
        parent_order_number = OrderNumber.objects.get(order_number = input_order_number)
        
        rf_ship_order = read_frame(Order.objects.filter(order_number=parent_order_number).order_by('id'))
        rf_item = read_frame(Item.objects.all(),fieldnames=[
            'item_code',
            'prj_code',
            'parts_name', 
            'parts_number', 
            'sell_price_cur',
            'sell_price',
            'buy_price_cur',
            'buy_price'
        ])
        
        rf_project = read_frame(Project.objects.all(), fieldnames=[
            'prj_code',
            'customer'
        ])
        
        data1 = pd.merge(rf_ship_order, rf_item, on='item_code', how='left')
        data1 = pd.merge(data1, rf_project, on='prj_code', how='inner')
             
        data2 = data1.to_dict()
    
        return JsonResponse({'ship_order_list':data2}, status=200)

class ShipmentComplete(LoginRequiredMixin,View):
    def post(self, request):
        order_id = request.POST.getlist('orderId', None)
        item_code_list = request.POST.getlist('shipItem', None)
        ship_date_list = request.POST.getlist('shipDate2', None)
        ship_qty_list = request.POST.getlist('shipQty', None)
        
        for i in range(len(ship_qty_list)):
            if ship_qty_list[i] == "":
                pass
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
            item_data = Item.objects.get(item_code=item_code_list[i])
            if ship_qty_list[i] == '':
                pass
            else:
                order_data.shipment_qty += int(ship_qty_list[i])
                order_data.stock -= int(ship_qty_list[i])
                order_data.save()
                item_data.stock -= int(ship_qty_list[i])
                item_data.save()
                
        return JsonResponse({'result':True}, status=200)
    
class ShipmentUpdateDataGet(LoginRequiredMixin,View):
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
            'parts_name', 
            'parts_number', 
            'sell_price_cur',
            'sell_price',
            'buy_price_cur',
            'buy_price'
        ])
        
        rf_project = read_frame(Project.objects.all(), fieldnames=[
            'prj_code',
            'customer'
        ])
        
  
        data1 = pd.merge(rf_ship_order, rf_item, on='item_code', how='left')
        data1 = pd.merge(data1, rf_project, on='prj_code', how='inner')
        print(data1)
        data2 = pd.merge(data1, rf_order, on='order_number', how='inner')
        
        data3 = data2.to_dict()
        return JsonResponse({'shipment_list':data3}, status=200)
        

class ShipmentUpdateConfirm(LoginRequiredMixin,View):
    def post(self,request):
        orderId_list = request.POST.getlist('orderId', None)
        item_code_list = request.POST.getlist('shipItem', None)
        ship_date_list = request.POST.getlist('shipDate2', None)
        shipId_list = request.POST.getlist('shipId', None)
        qty_list = request.POST.getlist('shipQty', None)
                
        for i in range (len(shipId_list)):
            parent_order = Order.objects.get(id=orderId_list[i])
            data = Shipment.objects.get(id=shipId_list[i])
            item_data = Item.objects.get(item_code=item_code_list[i])
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
                item_data.stock += int(original_qty)
                item_data.stock -= int(changed_qty)
                item_data.save()
            
        
        return JsonResponse({'result':True}, status=200)

class ShipmentDeleteConfirm(LoginRequiredMixin,View):
    def post(self, request):
        delete_check = request.POST.getlist('deleteCheckNum', None)
        orderId_list = request.POST.getlist('orderId', None)
        item_code_list = request.POST.getlist('shipItem', None)
        shipId_list = request.POST.getlist('shipId', None)
          
        for i in range (len(shipId_list)):
            if delete_check[i] == "1":
                parent_order = Order.objects.get(id=orderId_list[i])
                data = Shipment.objects.get(id=shipId_list[i])
                item_data = Item.objects.get(item_code=item_code_list[i])
                original_qty = data.shipment_qty
                parent_order.shipment_qty -= int(original_qty)
                parent_order.stock += int(original_qty)
                parent_order.save()
                data.delete()
                item_data.stock += int(original_qty)
                item_data.save()
                
            else:
                pass
            
        return JsonResponse({'result':True}, status=200)
    


### Acceptance ########################### 
class AcceptanceEntryView(LoginRequiredMixin,View):
    def get(self, request):
        user = request.user
        context = {'user':user}
        return render(request, 'omsapp/acceptance_entry.html', context)
    
class AcceptanceDataGet(LoginRequiredMixin,View):
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
            'sell_price_cur',
            'sell_price',
            'buy_price_cur',
            'buy_price'
        ])
        
        rf_project = read_frame(Project.objects.all(), fieldnames=[
            'prj_code',
            'customer'
        ])
        
   
        data1 = pd.merge(rf_accept_order, rf_item, on='item_code', how='left')
        data1 = pd.merge(data1, rf_project, on='prj_code', how='inner')
        
        data2 = data1.to_dict()
    
        return JsonResponse({'accept_order_list':data2}, status=200)
      
class AcceptanceComplete(LoginRequiredMixin,View):
    def post(self, request):
        input_order_number = request.POST.get('orderNumber', None)
        order_id = request.POST.getlist('orderId', None)
        item_code_list = request.POST.getlist('acceptItem', None)
        accept_date_list = request.POST.getlist('acceptDate2', None)
        accept_qty_list = request.POST.getlist('acceptQty', None)
        
        for i in range(len(accept_qty_list)):
            if accept_qty_list[i] == "":
                pass
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
            item_data = Item.objects.get(item_code=item_code_list[i])
            if accept_qty_list[i] == '':
                pass
            else:
                order_data.acceptance_qty += int(accept_qty_list[i])
                order_data.stock += int(accept_qty_list[i])
                order_data.balance -= int(accept_qty_list[i])
                order_data.save()
                item_data.stock += int(accept_qty_list[i])
                item_data.save()
        
        return JsonResponse({'result':True}, status=200)
    

class AcceptanceUpdateDataGet(LoginRequiredMixin,View):
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
            'sell_price_cur',
            'sell_price',
            'buy_price_cur',
            'buy_price'
        ])
        
        rf_project = read_frame(Project.objects.all(), fieldnames=[
            'prj_code',
            'customer'
        ])
        
   
        data1 = pd.merge(rf_accept_order, rf_item, on='item_code', how='left')
        data1 = pd.merge(data1, rf_project, on='prj_code', how='inner')
              
        data2 = pd.merge(data1, rf_order, on='order_number', how='inner')
        data3 = data2.to_dict()
        return JsonResponse({'acceptance_list':data3}, status=200)
   

class AcceptanceUpdateConfirm(LoginRequiredMixin,View):
    def post(self,request):
        orderId_list = request.POST.getlist('orderId', None)
        item_code_list = request.POST.getlist('acceptItem', None)
        accept_date_list = request.POST.getlist('acceptDate2', None)
        acceptId_list = request.POST.getlist('acceptId', None)
        qty_list = request.POST.getlist('acceptQty', None)
                
        for i in range (len(acceptId_list)):
            parent_order = Order.objects.get(id=orderId_list[i])
            data = Acceptance.objects.get(id=acceptId_list[i])
            item_data = Item.objects.get(item_code=item_code_list[i])
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
            item_data.stock -= int(original_qty)
            item_data.stock += int(changed_qty)
            item_data.save()


        return JsonResponse({'result':True}, status=200)

class AcceptanceDeleteConfirm(LoginRequiredMixin,View):
    def post(self, request):
        delete_check = request.POST.getlist('deleteCheckNum', None)
        orderId_list = request.POST.getlist('orderId', None)
        item_code_list = request.POST.getlist('acceptItem', None)
        acceptId_list = request.POST.getlist('acceptId', None)
        
        for i in range (len(acceptId_list)):
            if delete_check[i] == "1":
                parent_order = Order.objects.get(id=orderId_list[i])
                data = Acceptance.objects.get(id=acceptId_list[i])
                item_data = Item.objects.get(item_code=item_code_list[i])
                original_qty = data.acceptance_qty
                parent_order.acceptance_qty -= int(original_qty)
                parent_order.balance += int(original_qty)
                parent_order.stock -= int(original_qty)
                parent_order.save()
                data.delete()
                item_data.stock -= int(original_qty)
                item_data.save()
            else:
                pass
        return JsonResponse({'result':True}, status=200)



### Order Info ########################### 
class OrderInfoView(LoginRequiredMixin,View):    
    def get(self, request):   
        input_prj_code = request.GET.get('prjCode', None)
        input_order_number = request.GET.get('orderNum', None)
        input_order_date_s = request.GET.get('orderDateS', None)
        input_order_date_e = request.GET.get('orderDateE', None)    
        export = request.GET.get('export', None)
    
        rf_order = read_frame(Order.objects.all().order_by('id'))
     
        rf_item = read_frame(Item.objects.all(),fieldnames=[
            'item_code',
            'prj_code', 
            'supplier', 
            'parts_name', 
            'parts_number', 
            'sell_price_cur',
            'sell_price',
            'buy_price_cur',
            'buy_price'
        ])
        
        rf_project = read_frame(Project.objects.all(), fieldnames=[
            'prj_code',
            'customer'
        ])
        
        data1 = pd.merge(rf_order, rf_item, on='item_code', how='inner')
        data1 = pd.merge(data1, rf_project, on='prj_code', how='inner')
        
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

        data2 = data2.loc[:,[
            'id','prj_code','order_number','date_created','customer','item_code','parts_name','parts_number','supplier',
            'quantity','shipment_qty','acceptance_qty','stock','balance',
            'sell_price_cur','sell_price','buy_price_cur','buy_price','supplier_delivery_date','customer_delivery_date','user'
            ]]
        
 
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
            if export is None:
                return render(request, 'omsapp/order_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(order_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'order_number',
                                'item_code',
                                'quantity',
                                'supplier_delivery_date',
                                'customer_delivery_date',
                                'shipment_qty',
                                'acceptance_qty',
                                'balance',
                                'stock',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'buy_price_cur',
                                'buy_price',
                                'customer',
                                'user',
                                'date_created'
                                ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'order_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 
            
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
            if export is None:
                return render(request, 'omsapp/order_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(order_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'order_number',
                                'item_code',
                                'quantity',
                                'supplier_delivery_date',
                                'customer_delivery_date',
                                'shipment_qty',
                                'acceptance_qty',
                                'balance',
                                'stock',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'buy_price_cur',
                                'buy_price',
                                'customer',
                                'user',
                                'date_created'
                                ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'order_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 
            
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
            if export is None:
                return render(request, 'omsapp/order_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(order_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'order_number',
                                'item_code',
                                'quantity',
                                'supplier_delivery_date',
                                'customer_delivery_date',
                                'shipment_qty',
                                'acceptance_qty',
                                'balance',
                                'stock',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'buy_price_cur',
                                'buy_price',
                                'customer',
                                'user',
                                'date_created'
                                ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'order_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 
            
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
            if export is None:
                return render(request, 'omsapp/order_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(order_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'order_number',
                                'item_code',
                                'quantity',
                                'supplier_delivery_date',
                                'customer_delivery_date',
                                'shipment_qty',
                                'acceptance_qty',
                                'balance',
                                'stock',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'buy_price_cur',
                                'buy_price',
                                'customer',
                                'user',
                                'date_created'
                                ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'order_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 
            
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
            if export is None:
                return render(request, 'omsapp/order_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(order_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'order_number',
                                'item_code',
                                'quantity',
                                'supplier_delivery_date',
                                'customer_delivery_date',
                                'shipment_qty',
                                'acceptance_qty',
                                'balance',
                                'stock',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'buy_price_cur',
                                'buy_price',
                                'customer',
                                'user',
                                'date_created'
                                ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'order_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 
        
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
            if export is None:
                return render(request, 'omsapp/order_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(order_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'order_number',
                                'item_code',
                                'quantity',
                                'supplier_delivery_date',
                                'customer_delivery_date',
                                'shipment_qty',
                                'acceptance_qty',
                                'balance',
                                'stock',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'buy_price_cur',
                                'buy_price',
                                'customer',
                                'user',
                                'date_created'
                                ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'order_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 
        
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
            if export is None:
                return render(request, 'omsapp/order_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(order_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'order_number',
                                'item_code',
                                'quantity',
                                'supplier_delivery_date',
                                'customer_delivery_date',
                                'shipment_qty',
                                'acceptance_qty',
                                'balance',
                                'stock',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'buy_price_cur',
                                'buy_price',
                                'customer',
                                'user',
                                'date_created'
                                ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'order_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 
            
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
            if export is None:
                return render(request, 'omsapp/order_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(order_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'order_number',
                                'item_code',
                                'quantity',
                                'supplier_delivery_date',
                                'customer_delivery_date',
                                'shipment_qty',
                                'acceptance_qty',
                                'balance',
                                'stock',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'buy_price_cur',
                                'buy_price',
                                'customer',
                                'user',
                                'date_created'
                                ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'order_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 
        
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
            if export is None:
                return render(request, 'omsapp/order_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(order_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'order_number',
                                'item_code',
                                'quantity',
                                'supplier_delivery_date',
                                'customer_delivery_date',
                                'shipment_qty',
                                'acceptance_qty',
                                'balance',
                                'stock',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'buy_price_cur',
                                'buy_price',
                                'customer',
                                'user',
                                'date_created'
                                ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'order_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 
            
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
            if export is None:
                return render(request, 'omsapp/order_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(order_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'order_number',
                                'item_code',
                                'quantity',
                                'supplier_delivery_date',
                                'customer_delivery_date',
                                'shipment_qty',
                                'acceptance_qty',
                                'balance',
                                'stock',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'buy_price_cur',
                                'buy_price',
                                'customer',
                                'user',
                                'date_created'
                                ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'order_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 
            
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
            
            if export is None:
                return render(request, 'omsapp/order_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(order_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'order_number',
                                'item_code',
                                'quantity',
                                'supplier_delivery_date',
                                'customer_delivery_date',
                                'shipment_qty',
                                'acceptance_qty',
                                'balance',
                                'stock',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'buy_price_cur',
                                'buy_price',
                                'customer',
                                'user',
                                'date_created'
                                ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'order_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 

                            
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
            if export is None:
                return render(request, 'omsapp/order_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(order_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'order_number',
                                'item_code',
                                'quantity',
                                'supplier_delivery_date',
                                'customer_delivery_date',
                                'shipment_qty',
                                'acceptance_qty',
                                'balance',
                                'stock',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'buy_price_cur',
                                'buy_price',
                                'customer',
                                'user',
                                'date_created'
                                ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'order_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 

### Acceptance Info ########################### 
class AcceptanceInfoView(LoginRequiredMixin,View):
    def get(self, request):   
        input_prj_code = request.GET.get('prjCode', None)
        input_order_number = request.GET.get('orderNum', None)
        input_accept_date_s = request.GET.get('acceptDateS', None)
        input_accept_date_e = request.GET.get('acceptDateE', None)
        export = request.GET.get('export', None)
  

        rf_acceptance = read_frame(Acceptance.objects.all().order_by('id'))

        rf_item = read_frame(Item.objects.all(),fieldnames=[
            'item_code',
            'prj_code', 
            'supplier', 
            'parts_name', 
            'parts_number', 
            'buy_price_cur',
            'buy_price'
        ])
        
        data1 = pd.merge(
            rf_acceptance.sort_values('accepted_date'), 
            rf_item, 
            on='item_code', 
            how='left'
            )
      
        
        data2 = data1
        
        data2['amount'] = data2['acceptance_qty'] * data2['buy_price']
        data2 = data2.loc[:,['id', 'user','order_number','item_code','acceptance_qty','accepted_date','prj_code','parts_name','parts_number','buy_price_cur','buy_price','amount','supplier']]
        print(data2)


       # 1. prj_code only
        if input_prj_code != "" and input_order_number == "" and input_accept_date_s == "" and input_accept_date_e == "":
            accept_list = data2[data2['prj_code']==input_prj_code]
            context = {
                'accept_list':accept_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'accept_date_s':input_accept_date_s,
                'accept_date_e':input_accept_date_e
                }
            print('1')            
            if export is None:
                return render(request, 'omsapp/acceptance_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(accept_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'acceptance_qty',
                                'accepted_date',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'buy_price_cur',
                                'buy_price',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'acceptance_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 
            
        # 2. Order_No. only
        elif input_prj_code == "" and input_order_number != "" and input_accept_date_s == "" and input_accept_date_e == "":
            accept_list = data2[data2['order_number']==input_order_number]
            context = {
                'accept_list':accept_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'accept_date_s':input_accept_date_s,
                'accept_date_e':input_accept_date_e
                }
            print('2')
            if export is None:
                return render(request, 'omsapp/acceptance_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(accept_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'acceptance_qty',
                                'accepted_date',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'buy_price_cur',
                                'buy_price',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'acceptance_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response  
                        
        # 3. order_date_s only
        elif input_prj_code == "" and input_order_number == "" and input_accept_date_s != "" and input_accept_date_e == "":
            accept_date_s = pd.to_datetime(input_accept_date_s).floor('D')
            accept_list = data2[data2['accepted_date']>=accept_date_s]         
            context = {
                'accept_list':accept_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'accept_date_s':input_accept_date_s,
                'accept_date_e':input_accept_date_e
                }
            print('3')
            if export is None:
                return render(request, 'omsapp/acceptance_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(accept_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'acceptance_qty',
                                'accepted_date',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'buy_price_cur',
                                'buy_price',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'acceptance_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 
                        
        # 4. order_date_e only
        elif input_prj_code == "" and input_order_number == "" and input_accept_date_s == "" and input_accept_date_e != "":
            accept_list = data2[data2['accepted_date']<=accept_date_s]
            context = {
                'accept_list':accept_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'accept_date_s':input_accept_date_s,
                'accept_date_e':input_accept_date_e
                }
            print('4')
            if export is None:
                return render(request, 'omsapp/acceptance_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(accept_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'acceptance_qty',
                                'accepted_date',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'buy_price_cur',
                                'buy_price',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'acceptance_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 
                        
        # 5. order_date_s and order_date_e
        elif input_prj_code == "" and input_order_number == "" and input_accept_date_s != "" and input_accept_date_e != "":
            accept_date_s = pd.to_datetime(input_accept_date_s).floor('D')
            accept_date_e = pd.to_datetime(input_accept_date_e).floor('D')
            data3 = data2[data2['accepted_date']>=accept_date_s]
            accept_list = data3[data3['accepted_date']<=accept_date_e]
            context = {
                'accept_list':accept_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'accept_date_s':input_accept_date_s,
                'accept_date_e':input_accept_date_e
                }
            print('5')
            if export is None:
                return render(request, 'omsapp/acceptance_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(accept_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'acceptance_qty',
                                'accepted_date',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'buy_price_cur',
                                'buy_price',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'acceptance_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 
                    
        # 6. prj_code and Order_No
        elif input_prj_code != "" and input_order_number != "" and input_accept_date_s == "" and input_accept_date_e == "":
            data3 = data2[data2['prj_code']==input_prj_code]
            accept_list = data3[data3['order_number']==input_order_number]
            context = {
                'accept_list':accept_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'accept_date_s':input_accept_date_s,
                'accept_date_e':input_accept_date_e
                }
            print('6')      
            if export is None:
                return render(request, 'omsapp/acceptance_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(accept_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'acceptance_qty',
                                'accepted_date',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'buy_price_cur',
                                'buy_price',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'acceptance_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 
                    
        # 7. prj_code and order_date_s
        elif input_prj_code != "" and input_order_number == "" and input_accept_date_s != "" and input_accept_date_e == "":
            accept_date_s = pd.to_datetime(input_accept_date_s).floor('D')
            data3 = data2[data2['prj_code']==input_prj_code]
            accept_list = data3[data3['accepted_date']>=accept_date_s]
            context = {
                'accept_list':accept_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'accept_date_s':input_accept_date_s,
                'accept_date_e':input_accept_date_e
                }
            print('7')      
            if export is None:
                return render(request, 'omsapp/acceptance_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(accept_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'acceptance_qty',
                                'accepted_date',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'buy_price_cur',
                                'buy_price',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'acceptance_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 
                        
        # 8. prj_code and order_date_s and order_date_e
        elif input_prj_code != "" and input_order_number == "" and input_accept_date_s != "" and input_accept_date_e != "":
            accept_date_s = pd.to_datetime(input_accept_date_s).floor('D')
            accept_date_e = pd.to_datetime(input_accept_date_e).floor('D')
            data3 = data2[data2['prj_code']==input_prj_code]
            data4 = data3[data3['accepted_date']>=accept_date_s]
            accept_list = data4[data4['accepted_date']<=accept_date_e]
            context = {
                'accept_list':accept_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'accept_date_s':input_accept_date_s,
                'accept_date_e':input_accept_date_e
                }
            print('8')      
            if export is None:
                return render(request, 'omsapp/acceptance_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(accept_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'acceptance_qty',
                                'accepted_date',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'buy_price_cur',
                                'buy_price',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'acceptance_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 
                    
        # 9. Order_No and order_date_s
        elif input_prj_code == "" and input_order_number != "" and input_accept_date_s != "" and input_accept_date_e == "":
            accept_date_s = pd.to_datetime(input_order_date_s).floor('D')
            data3 = data2[data2['order_number']==input_order_number]
            accept_list = data3[data3['accepted_date']>=accept_date_s]
            context = {
                'accept_list':accept_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'accept_date_s':input_accept_date_s,
                'accept_date_e':input_accept_date_e
                }
            print('9')      
            if export is None:
                return render(request, 'omsapp/acceptance_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(accept_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'acceptance_qty',
                                'accepted_date',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'buy_price_cur',
                                'buy_price',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'acceptance_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 
                    
        # 10. Order_No and order_date_s and order_date_e
        elif input_prj_code == "" and input_order_number != "" and input_accept_date_s != "" and input_accept_date_e != "":
            accept_date_s = pd.to_datetime(input_order_date_s).floor('D')
            accept_date_e = pd.to_datetime(input_order_date_e).floor('D')
            data3 = data2[data2['order_number']==input_order_number]
            data4 = data3[data3['accepted_date']>=accept_date_s]
            accept_list = data4[data4['accepted_date']<=accept_date_e]
            context = {
                'accept_list':accept_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'accept_date_s':input_accept_date_s,
                'accept_date_e':input_accept_date_e
                }
            print('10')      
            if export is None:
                return render(request, 'omsapp/acceptance_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(accept_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'acceptance_qty',
                                'accepted_date',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'buy_price_cur',
                                'buy_price',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'acceptance_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 
                    
        
        # 11. No input
        elif input_prj_code == "" and input_order_number == "" and input_accept_date_s == "" and input_accept_date_e == "":
            accept_list = data2 
            context = {
                'accept_list':accept_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'accept_date_s':input_accept_date_s,
                'accept_date_e':input_accept_date_e
                }
            print('11')
            if export is None:
                return render(request, 'omsapp/acceptance_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(accept_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'acceptance_qty',
                                'accepted_date',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'buy_price_cur',
                                'buy_price',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'acceptance_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 
                    
        # 12. default
        elif input_prj_code is None and input_order_number is None and input_accept_date_s is None and input_accept_date_e is None:
            print('12')            
            return render(request, 'omsapp/acceptance_info.html')
        
        # 13. All Input 
        else:
            accept_date_s = pd.to_datetime(input_accept_date_s).floor('D')
            accept_date_e = pd.to_datetime(input_accept_date_e).floor('D')
            data3 = data2[data2['prj_code']==input_prj_code]
            data4 = data3[data3['order_number']==input_order_number]
            data5 = data4[data4['accepted_date']>=accept_date_s]
            order_list = data5[data5['accepted_date']<=accept_date_e]
            context = {
                'accept_list':accept_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'accept_date_s':input_accept_date_s,
                'accept_date_e':input_accept_date_e
                }
            print('13')      
            if export is None:
                    return render(request, 'omsapp/acceptance_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(accept_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2', 
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'acceptance_qty',
                                'accepted_date',
                                'prj_code',
                                'supplier',
                                'parts_name',
                                'parts_number',
                                'buy_price_cur',
                                'buy_price',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'acceptance_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response  
            
### Shipment Info ########################### 
class ShipmentInfoView(LoginRequiredMixin,View):
    def get(self, request):   
        input_prj_code = request.GET.get('prjCode', None)
        input_order_number = request.GET.get('orderNum', None)
        input_ship_date_s = request.GET.get('shipDateS', None)
        input_ship_date_e = request.GET.get('shipDateE', None) 
        export = request.GET.get('export', None)

        rf_shipment = read_frame(Shipment.objects.all().order_by('id'))

        rf_item = read_frame(Item.objects.all(),fieldnames=[
            'item_code',
            'prj_code', 
            'parts_name', 
            'parts_number', 
            'sell_price_cur',
            'sell_price'
        ])
        
        rf_project = read_frame(Project.objects.all(), fieldnames=[
            'prj_code',
            'customer'
        ])
        
   
        
        data1 = pd.merge(
            rf_shipment, 
            rf_item, 
            on='item_code', 
            how='left'
            )
      
        data1 = pd.merge(data1.sort_values('shipped_date'), rf_project, on='prj_code', how='inner')
        
        data2 = data1
        
        data2['amount'] = data2['shipment_qty'] * data2['sell_price']
        data2 = data2.loc[:,['id','user','order_number','item_code','shipment_qty','shipped_date','prj_code','parts_name','parts_number','sell_price_cur','sell_price', 'amount','customer']]
        print(data2)


        # 1. prj_code only
        if input_prj_code != "" and input_order_number == "" and input_ship_date_s == "" and input_ship_date_e == "":
            ship_list = data2[data2['prj_code']==input_prj_code]
            context = {
                'ship_list':ship_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'ship_date_s':input_ship_date_s,
                'ship_date_e':input_ship_date_e
                }
            print('1')
            if export is None:
                    return render(request, 'omsapp/shipment_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(ship_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2',
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'shipment_qty',
                                'shipped_date',
                                'prj_code',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'customer',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'shipment_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response 

            
        # 2. Order_No. only
        elif input_prj_code == "" and input_order_number != "" and input_ship_date_s == "" and input_ship_date_e == "":
            ship_list = data2[data2['order_number']==input_order_number]
            context = {
                'ship_list':ship_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'ship_date_s':input_ship_date_s,
                'ship_date_e':input_ship_date_e
                }
            print('2')
            if export is None:
                    return render(request, 'omsapp/shipment_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(ship_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2',
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'shipment_qty',
                                'shipped_date',
                                'prj_code',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'customer',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'shipment_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response  
            
        # 3. order_date_s only
        elif input_prj_code == "" and input_order_number == "" and input_ship_date_s != "" and input_ship_date_e == "":
            ship_date_s = pd.to_datetime(input_ship_date_s).floor('D')
            ship_list = data2[data2['shipped_date']>=ship_date_s]         
            context = {
                'ship_list':ship_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'ship_date_s':input_ship_date_s,
                'ship_date_e':input_ship_date_e
                }
            print('3')
            if export is None:
                    return render(request, 'omsapp/shipment_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(ship_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2',
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'shipment_qty',
                                'shipped_date',
                                'prj_code',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'customer',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'shipment_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response  
            
        # 4. order_date_e only
        elif input_prj_code == "" and input_order_number == "" and input_ship_date_s == "" and input_ship_date_e != "":
            ship_list = data2[data2['shipped_date']<=ship_date_s]
            context = {
                'ship_list':ship_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'ship_date_s':input_ship_date_s,
                'ship_date_e':input_ship_date_e
                }
            print('4')
            if export is None:
                    return render(request, 'omsapp/shipment_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(ship_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2',
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'shipment_qty',
                                'shipped_date',
                                'prj_code',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'customer',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'shipment_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response  
            
        # 5. order_date_s and order_date_e
        elif input_prj_code == "" and input_order_number == "" and input_ship_date_s != "" and input_ship_date_e != "":
            ship_date_s = pd.to_datetime(input_ship_date_s).floor('D')
            ship_date_e = pd.to_datetime(input_ship_date_e).floor('D')
            data3 = data2[data2['shipped_date']>=ship_date_s]
            ship_list = data3[data3['shipped_date']<=ship_date_e]
            context = {
                'ship_list':ship_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'ship_date_s':input_ship_date_s,
                'ship_date_e':input_ship_date_e
                }
            print('5')
            if export is None:
                    return render(request, 'omsapp/shipment_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(ship_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2',
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'shipment_qty',
                                'shipped_date',
                                'prj_code',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'customer',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'shipment_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response  
        
        # 6. prj_code and Order_No
        elif input_prj_code != "" and input_order_number != "" and input_ship_date_s == "" and input_ship_date_e == "":
            data3 = data2[data2['prj_code']==input_prj_code]
            ship_list = data3[data3['order_number']==input_order_number]
            context = {
                'ship_list':ship_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'ship_date_s':input_ship_date_s,
                'ship_date_e':input_ship_date_e
                }
            print('6')      
            if export is None:
                    return render(request, 'omsapp/shipment_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(ship_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2',
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'shipment_qty',
                                'shipped_date',
                                'prj_code',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'customer',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'shipment_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response  
        
        # 7. prj_code and order_date_s
        elif input_prj_code != "" and input_order_number == "" and input_ship_date_s != "" and input_ship_date_e == "":
            ship_date_s = pd.to_datetime(input_ship_date_s).floor('D')
            data3 = data2[data2['prj_code']==input_prj_code]
            ship_list = data3[data3['shipped_date']>=ship_date_s]
            context = {
                'ship_list':ship_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'ship_date_s':input_ship_date_s,
                'ship_date_e':input_ship_date_e
                }
            print('7')      
            if export is None:
                    return render(request, 'omsapp/shipment_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(ship_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2',
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'shipment_qty',
                                'shipped_date',
                                'prj_code',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'customer',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'shipment_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response  
            
        # 8. prj_code and order_date_s and order_date_e
        elif input_prj_code != "" and input_order_number == "" and input_ship_date_s != "" and input_ship_date_e != "":
            ship_date_s = pd.to_datetime(input_ship_date_s).floor('D')
            ship_date_e = pd.to_datetime(input_ship_date_e).floor('D')
            data3 = data2[data2['prj_code']==input_prj_code]
            data4 = data3[data3['shipped_date']>=ship_date_s]
            ship_list = data4[data4['shipped_date']<=ship_date_e]
            context = {
                'ship_list':ship_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'ship_date_s':input_ship_date_s,
                'ship_date_e':input_ship_date_e
                }
            print('8')      
            if export is None:
                    return render(request, 'omsapp/shipment_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(ship_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2',
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'shipment_qty',
                                'shipped_date',
                                'prj_code',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'customer',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'shipment_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response  
        
        # 9. Order_No and order_date_s
        elif input_prj_code == "" and input_order_number != "" and input_ship_date_s != "" and input_ship_date_e == "":
            ship_date_s = pd.to_datetime(input_ship_date_s).floor('D')
            data3 = data2[data2['order_number']==input_order_number]
            ship_list = data3[data3['shipped_date']>=ship_date_s]
            context = {
                'ship_list':ship_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'ship_date_s':input_ship_date_s,
                'ship_date_e':input_ship_date_e
                }
            print('9')      
            if export is None:
                    return render(request, 'omsapp/shipment_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(ship_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2',
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'shipment_qty',
                                'shipped_date',
                                'prj_code',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'customer',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'shipment_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response  
        
        # 10. Order_No and order_date_s and order_date_e
        elif input_prj_code == "" and input_order_number != "" and input_ship_date_s != "" and input_ship_date_e != "":
            ship_date_s = pd.to_datetime(input_ship_date_s).floor('D')
            ship_date_e = pd.to_datetime(input_ship_date_e).floor('D')
            data3 = data2[data2['order_number']==input_order_number]
            data4 = data3[data3['shipped_date']>=ship_date_s]
            ship_list = data4[data4['shipped_date']<=ship_date_e]
            context = {
                'ship_list':ship_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'ship_date_s':input_ship_date_s,
                'ship_date_e':input_ship_date_e
                }
            print('10')      
            if export is None:
                    return render(request, 'omsapp/shipment_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(ship_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2',
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'shipment_qty',
                                'shipped_date',
                                'prj_code',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'customer',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'shipment_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response  
        
        # 11. No input
        elif input_prj_code == "" and input_order_number == "" and input_ship_date_s == "" and input_ship_date_e == "":
            ship_list = data2 
            context = {
                'ship_list':ship_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'ship_date_s':input_ship_date_s,
                'ship_date_e':input_ship_date_e
                }
            print('11')      
            if export is None:
                    return render(request, 'omsapp/shipment_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(ship_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2',
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'shipment_qty',
                                'shipped_date',
                                'prj_code',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'customer',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'shipment_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response  

        
        # 12. default
        elif input_prj_code is None and input_order_number is None and input_ship_date_s is None and input_ship_date_e is None:
            print('12')            
            return render(request, 'omsapp/shipment_info.html')
        
        # 13. All Input 
        else:
            ship_date_s = pd.to_datetime(input_ship_date_s).floor('D')
            ship_date_e = pd.to_datetime(input_ship_date_e).floor('D')
            data3 = data2[data2['prj_code']==input_prj_code]
            data4 = data3[data3['order_number']==input_order_number]
            data5 = data4[data4['shipped_date']>=ship_date_s]
            order_list = data5[data5['shipped_date']<=ship_date_e]
            context = {
                'ship_list':ship_list, 
                'prj_code':input_prj_code, 
                'order_number':input_order_number,
                'ship_date_s':input_ship_date_s,
                'ship_date_e':input_ship_date_e
                }
            print('13')      
            if export is None:
                    return render(request, 'omsapp/shipment_info.html',context)
            else:
                bio = BytesIO()
                writer = StyleFrame.ExcelWriter(bio)
                sf = StyleFrame(ship_list)
                sf.to_excel(writer, 
                            sheet_name='sheet1', 
                            index=False, columns_and_rows_to_freeze='B2',
                            best_fit=[
                                'id',
                                'user',
                                'order_number',
                                'item_code',
                                'shipment_qty',
                                'shipped_date',
                                'prj_code',
                                'parts_name',
                                'parts_number',
                                'sell_price_cur',
                                'sell_price',
                                'customer',
                                'amount'
                            ]
                            )
                writer.save()
                bio.seek(0)
                workbook = bio.read()
                file_name = 'shipment_info.xlsx'
                response = HttpResponse(workbook, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response  

### Inventory Info ########################### 
class ItemInfoView(LoginRequiredMixin,View):
    def get(self, request):
        input_prj_code = request.GET.get('prjCode', None)
        input_item_code = request.GET.get('itemCode', None)
        input_parts_num = request.GET.get('partsNumber', None) 

        rf_item = read_frame(Item.objects.all())
        
        rf_project = read_frame(Project.objects.all(), fieldnames=[
            'prj_code',
            'customer'
        ])

        data1 = pd.merge(rf_item, rf_project, on='prj_code', how='inner')
            
        data1['amount'] = data1['stock'] * data1['buy_price']
        
        
        print(data1)
        
        # 1. Prj Code
        if input_prj_code != "" and input_item_code == "" and input_parts_num == "":
            item_list = data1[data1['prj_code']==input_prj_code]
            context = {
                'item_list':item_list, 
                'prj_code':input_prj_code, 
                'item_code':input_item_code,
                'parts_num':input_parts_num
                }
            print('1')
            return render(request, 'omsapp/item_info.html', context)

        # 2. Item Code
        elif input_prj_code == "" and input_item_code != "" and input_parts_num == "":
            item_list = data1[data1['item_code']==input_item_code]
            context = {
                'item_list':item_list, 
                'prj_code':input_prj_code, 
                'item_code':input_item_code,
                'parts_num':input_parts_num
                }
            print('2')
            return render(request, 'omsapp/item_info.html', context)
            
        # 3. P/N
        elif input_prj_code == "" and input_item_code == "" and input_parts_num != "":
            item_list = data1[data1['parts_number']==input_parts_num]
            context = {
                'item_list':item_list, 
                'prj_code':input_prj_code, 
                'item_code':input_item_code,
                'parts_num':input_parts_num
                }
            print('3')
            return render(request, 'omsapp/item_info.html', context)
            
        # 4. Prj Code & Item Code
        elif input_prj_code != "" and input_item_code != "" and input_parts_num == "":
            data2 = data1[data1['prj_code']==input_prj_code]
            item_list = data2[data2['item_code']==input_item_code]
            context = {
                'item_list':item_list, 
                'prj_code':input_prj_code, 
                'item_code':input_item_code,
                'parts_num':input_parts_num
                }
            print('4')
            return render(request, 'omsapp/item_info.html', context)
            
        # 5. Prj Code & P/N
        elif input_prj_code != "" and input_item_code == "" and input_parts_num != "":
            data2 = data1[data1['prj_code']==input_prj_code]
            item_list = data2[data2['parts_number']==input_parts_num]
            context = {
                'item_list':item_list, 
                'prj_code':input_prj_code, 
                'item_code':input_item_code,
                'parts_num':input_parts_num
                }
            print('5')
            return render(request, 'omsapp/item_info.html', context)
        
        # 6. Item Code & P/N
        elif input_prj_code == "" and input_item_code != "" and input_parts_num != "":
            data2 = data1[data1['item_code']==input_item_code]
            item_list = data2[data2['parts_number']==input_parts_num]
            context = {
                'item_list':item_list, 
                'prj_code':input_prj_code, 
                'item_code':input_item_code,
                'parts_num':input_parts_num
                }
            print('6')
            return render(request, 'omsapp/item_info.html', context)
            
        # 7. No Input()
        elif input_prj_code == "" and input_item_code == "" and input_parts_num == "":
            item_list = data1
            context = {
                'item_list':item_list, 
                'prj_code':input_prj_code, 
                'item_code':input_item_code,
                'parts_num':input_parts_num
                }
            print('7')
            return render(request, 'omsapp/item_info.html', context)
            
        # 8. default()
        elif input_prj_code is None and input_item_code is None and input_parts_num is None : 
            print('8')
            return render(request, 'omsapp/item_info.html')
    
        # 9. All Input()
        else:
            data2 = data1[data1['prj_code']==input_prj_code]
            data3 = data2[data2['item_code']==input_item_code]
            item_list = data3[data3['parts_number']==input_parts_num]
            context = {
                'item_list':item_list, 
                'prj_code':input_prj_code, 
                'item_code':input_item_code,
                'parts_num':input_parts_num
                }
            print('9')
            return render(request, 'omsapp/item_info.html', context)
            


### Admin Only ####################################### 
decorators = [admin_only]

@method_decorator(decorators, name='dispatch')
class ItemCreateView(LoginRequiredMixin,View):
    def get(self,request):
        sell_cur_list = Currency_S.objects.all()
        buy_cur_list = Currency_B.objects.all()
        
        context = {'sell_cur_list':sell_cur_list, 'buy_cur_list':buy_cur_list}
        return render(request, 'omsapp/item_create.html', context)
    
    def post(self, request):
        input_prj_code = request.POST.get('prjCode', None)
        input_supplier_code = request.POST.get('supplier', None)
        input_parts_name = request.POST.get('partsName', None)
        input_parts_number = request.POST.get('partsNum', None)
        input_sell_price = request.POST.get('sellPrice', None)
        input_buy_price = request.POST.get('buyPrice', None)
        
        input_sell_cur = request.POST.get('sellCur', None)
        input_buy_cur = request.POST.get('buyCur', None)
        
        sell_cur = Currency_S.objects.get(currency=input_sell_cur)
        buy_cur = Currency_B.objects.get(currency=input_buy_cur)
        
        new_item = Item.objects.create(
            prj_code = Project.objects.get(prj_code=input_prj_code),
            supplier = Supplier.objects.get(supplier_code=input_supplier_code),
            parts_name = input_parts_name,
            parts_number = input_parts_number,
            sell_price_cur = sell_cur,
            sell_price = input_sell_price,
            buy_price_cur = buy_cur,
            buy_price = input_buy_price
        )
        
        new_item_code = Item.objects.latest('item_code').item_code
        print(new_item_code)
        new_item = read_frame(Item.objects.filter(item_code=new_item_code))
        print(new_item)
        data1 = new_item.to_dict()
        
        return JsonResponse({'new_item':data1}, status=200)

@method_decorator(decorators, name='dispatch')
class ItemUpdateView(LoginRequiredMixin,View):
    def get(self,request):
        item_id = request.GET.get('dataId', None)
        update_item = Item.objects.get(id=item_id)
        
        return JsonResponse({'item':model_to_dict(update_item)}, status=200)
    
    def post(self,request):
        item_id = request.POST.get('itemId', None)
        sell_price = request.POST.get('sellPrice', None)
        buy_price = request.POST.get('buyPrice', None)
        delete_check = request.POST.get('deleteCheckNum', None)
        update_item = Item.objects.get(id=item_id)
        
        print(item_id)
        print(sell_price)
        print(buy_price)
        print(delete_check)
        print(update_item)
        
        if delete_check == "0":  #update 
            update_item.sell_price=sell_price
            update_item.buy_price=buy_price
            update_item.save()
            return JsonResponse({'result':model_to_dict(update_item)}, status=200)
            
        elif delete_check == "1": #delete
            update_item.delete()
            return JsonResponse({'result':'delete'}, status=200)  

@method_decorator(decorators, name='dispatch')
class CustomerCreateView(LoginRequiredMixin,CreateView):
    model = Customer
    form_class = CustomerCreateForm
    template_name = "omsapp/customer_create_form.html"
    success_url = reverse_lazy("customer_info")

@method_decorator(decorators, name='dispatch')
class CustomerUpdateView(LoginRequiredMixin,UpdateView):
    model = Customer
    form_class = CustomerCreateForm
    template_name = "omsapp/customer_update_form.html"
    success_url = reverse_lazy("customer_info")

@method_decorator(decorators, name='dispatch') 
class CustomerDeleteView(LoginRequiredMixin,DeleteView):
    model = Customer
    success_url = reverse_lazy("customer_info")

@method_decorator(decorators, name='dispatch')
class CustomerListView(LoginRequiredMixin,ListView):
    model = Customer

@method_decorator(decorators, name='dispatch')
class SupplierCreateView(LoginRequiredMixin,CreateView):
    model = Supplier
    form_class = SupplierCreateForm
    template_name = "omsapp/supplier_create_form.html"
    success_url = reverse_lazy("supplier_info")

@method_decorator(decorators, name='dispatch')
class SupplierUpdateView(LoginRequiredMixin,UpdateView):
    model = Supplier
    form_class = SupplierCreateForm
    template_name = "omsapp/supplier_update_form.html"
    success_url = reverse_lazy("supplier_info")

@method_decorator(decorators, name='dispatch')
class SupplierDeleteView(LoginRequiredMixin,DeleteView):
    model = Supplier
    success_url = reverse_lazy("supplier_info")

@method_decorator(decorators, name='dispatch')
class SupplierListView(LoginRequiredMixin,ListView):
    model = Supplier
    
@method_decorator(decorators, name='dispatch')
class ProjectCreateView(LoginRequiredMixin,CreateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = "omsapp/project_create_form.html"
    success_url = reverse_lazy("project_info")

@method_decorator(decorators, name='dispatch')
class ProjectUpdateView(LoginRequiredMixin,UpdateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = "omsapp/project_update_form.html"
    success_url = reverse_lazy("project_info")

@method_decorator(decorators, name='dispatch')
class ProjectDeleteView(LoginRequiredMixin,DeleteView):
    model = Project
    success_url = reverse_lazy("project_info")

@method_decorator(decorators, name='dispatch')     
class ProjectListView(LoginRequiredMixin,ListView):
    model = Project
    


