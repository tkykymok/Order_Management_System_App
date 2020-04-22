from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import (
    View,
    ListView,
    DetailView,
    UpdateView
)
from omsapp.models import Order, Item, OrderNumber, Order, Project, User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
# from extra_views import InlineFormSetFactory, CreateWithInlinesView, UpdateWithInlinesView
from django.views.generic import TemplateView
from .forms import OrderNumberForm, OrderForm

from django.http import JsonResponse
from django.forms.models import model_to_dict


class MenuView(View,LoginRequiredMixin):
    def get(self, request):
        return render(request, 'omsapp/menu.html')

    
class OrderCreateView(View, LoginRequiredMixin):
    def get(self,request):
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
        item_code = request.POST.getlist('item', None)
        item_info = Item.objects.get(item_code=item_code[-1])
        prj = item_info.prj_code.prj_code
        print(prj)
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
                new_order = Order.objects.create(
                    order_number = OrderNumber.objects.get(order_number=input_order_number),
                    item_code = Item.objects.get(item_code = items[i]),
                    quantity = qtys[i],
                    supplier_delivery_date = suppDates[i],
                    customer_delivery_date = custDates[i]
                )
                
            
        return JsonResponse({'result':'ok'}, status=200)

class OrderListView(View, LoginRequiredMixin):
    def get(self, request):
        order_list = Order.objects.all()
        context = {'order_list':order_list}
        return render(request, 'omsapp/order_list.html', context)
        
    def post(self, request):
        # delete_check_val = request.POST.get('deleteCheck')
        get_id = request.POST.get('formId', None)
        new_supp_del_date = request.POST.get('suppDelDate', None)
        new_cust_del_date = request.POST.get('custDelDate', None)
        new_qty = request.POST.get('qty', None)
                
        new_order = Order.objects.get(id=get_id)
        new_order.quantity = int(new_qty)
        new_order.supplier_delivery_date = new_supp_del_date
        new_order.customer_delivery_date = new_cust_del_date 
        new_order.save()        
            
        return JsonResponse({'new_order':model_to_dict(new_order)}, status=200)  
  
class OrderDelete(View):
    def get(self, request):
        get_id = request.GET.get('id', None)
        Order.objects.get(id=get_id).delete()
        return JsonResponse({'deleted':True}, status=200)
    
            
    

class OrderUpdate(View):
    def get(self, request, id):
        cur_order = Order.objects.get(id=id)
        return JsonResponse({'cur_order':model_to_dict(cur_order)}, status=200)
 



    
    
# class OrderUpdateView(UpdateView):
#     model = Order
#     form_class = OrderForm
    
#     template_name = 'omsapp/order_update.html'
#     success_url = reverse_lazy('success')
    
#     def form_valid(self, form):
#         result = super().form_valid(form)
#         return result

# class SuccessView(TemplateView):
#     template_name = "omsapp/success.html"
    
# class OrderDetailView(DetailView):
#     model = Order
#     template_name = "omsapp/order_detail.html"
    
# class OrderListView(ListView, LoginRequiredMixin):
#     model = Order
#     template_name = 'omsapp/order_list.html'
#     context_object_name = 'orders'
#     ordering = ['order_number']
    

# class OrderInline(InlineFormSetFactory):
#     model = Order
#     fields = '__all__'
#     factory_kwargs = {'extra': 10}
    

# class OrderCreateView(CreateWithInlinesView):
#     model = OrderNumber
#     fields = ['order_number']
#     context_object_name = 'order_number'
#     inlines = [OrderInline]
#     template_name = 'omsapp/order_entry.html'
#     success_url = reverse_lazy('success')