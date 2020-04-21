from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import (
    View,
    ListView,
    DetailView,
    UpdateView
)
from omsapp.models import Order, Item, OrderNumber, Order, Project

from django.urls import reverse_lazy
# from extra_views import InlineFormSetFactory, CreateWithInlinesView, UpdateWithInlinesView
from django.views.generic import TemplateView
from .forms import OrderNumberForm, OrderForm


from django.http import JsonResponse
from django.forms.models import model_to_dict

class MenuView(View):
    def get(self, request):
        return render(request, 'omsapp/menu.html')

    
class OrderCreateView(View):
    def get(self,request):
        return render(request, 'omsapp/order_entry.html')

class PrjCodeGet(View):
    def post(self, request):
        prj_code_get = request.POST.getlist('prjCode', None)
        prj_code = Project.objects.get(prj_code = prj_code_get[0])
        customer_info = prj_code.customer_code
        return JsonResponse({'customer_info':model_to_dict(customer_info)}, status=200)
    
class OrderNumberCreate(View):
    def post(self, request):
        order_number = request.POST.get('orderNumber',None)
        supplier_delivery_date = request.POST.get('suppDelDate',None)
        customer_delivery_date = request.POST.get('custDelDate',None)
        new_order_number = OrderNumber(
            order_number=order_number,
            supplier_delivery_date=supplier_delivery_date,
            customer_delivery_date=customer_delivery_date)
        if order_number == "":
            return redirect ('order_entry')
        else:
            new_order_number.save()
        
        return JsonResponse({'orderNumber':model_to_dict(new_order_number)}, status=200)
        
class ItemInfoGet(View):
    def post(self, request):
        item_code = request.POST.getlist('item', None)
        item_info = Item.objects.get(item_code=item_code[-1])
        prj = item_info.prj_code.prj_code
        print(prj)
        return JsonResponse({'item_info':model_to_dict(item_info),'prj':prj}, status=200)
    
class OrderCreateConfirm(View):
    def post(self, request):
        input_order_number = request.POST.get('orderNumber', None)
    
        items = request.POST.getlist('item', None)
        qtys = request.POST.getlist('qty', None)
        
        for i in range(len(items)):
            if items[i] == "":
                break
            else:      
                new_order = Order.objects.create(
                    order_number = OrderNumber.objects.get(order_number=input_order_number),
                    item_code = Item.objects.get(item_code = items[i]),
                    quantity = qtys[i]
                )
                print(new_order)
            
        return JsonResponse({'result':'ok'}, status=200)
    
    
    
    
    
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
    
class OrderListView(ListView):
    model = Order
    template_name = 'omsapp/order_list.html'
    context_object_name = 'orders'
    ordering = ['order_number']
    

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