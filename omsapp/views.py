from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import (
    View,
    ListView,
    DetailView,
    UpdateView
)
from omsapp.models import Order, Item, OrderNumber, Order

from django.urls import reverse_lazy
from extra_views import InlineFormSetFactory, CreateWithInlinesView, UpdateWithInlinesView
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
    
class OrderNumberCreateView(View):
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
        
class ItemInfoGetView(View):
    def post(self, request):
            item_code = request.POST.getlist('item', None)
            item_info = Item.objects.get(item_code=item_code[0])
            print(vars(item_info))
            print(item_code)
            return JsonResponse({'item_info':model_to_dict(item_info)}, status=200)
        
        # elif request.POST.get('item2', None):
        #     item_code = request.POST.get('item2', None)
        #     item_info = Item.objects.get(item_code=item_code)
        #     print(vars(item_info))
        #     return JsonResponse({'item_info':model_to_dict(item_info)}, status=200)
        # elif request.POST.get('item3', None):
        #     item_code = request.POST.get('item3', None)
        #     item_info = Item.objects.get(item_code=item_code)
        #     print(vars(item_info))
        #     return JsonResponse({'item_info':model_to_dict(item_info)}, status=200)
        # elif request.POST.get('item4', None):
        #     item_code = request.POST.get('item4', None)
        #     item_info = Item.objects.get(item_code=item_code)
        #     print(vars(item_info))
        #     return JsonResponse({'item_info':model_to_dict(item_info)}, status=200)
        # elif request.POST.get('item5', None):
        #     item_code = request.POST.get('item5', None)
        #     item_info = Item.objects.get(item_code=item_code)
        #     print(vars(item_info))
        #     return JsonResponse({'item_info':model_to_dict(item_info)}, status=200)
            
        
    
        

# class UpdateCrudUser(View):
#     def  get(self, request):
#         id1 = request.GET.get('id', None)
#         name1 = request.GET.get('name', None)
#         address1 = request.GET.get('address', None)
#         age1 = request.GET.get('age', None)

#         obj = CrudUser.objects.get(id=id1)
#         obj.name = name1
#         obj.address = address1
#         obj.age = age1
#         obj.save()

#         user = {'id':obj.id,'name':obj.name,'address':obj.address,'age':obj.age}

#         data = {
#             'user': user
#         }
#         return JsonResponse(data)
        
        

    
    
    
    
    
class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    
    template_name = 'omsapp/order_update.html'
    success_url = reverse_lazy('success')
    
    def form_valid(self, form):
        result = super().form_valid(form)
        return result

class SuccessView(TemplateView):
    template_name = "omsapp/success.html"
    
class OrderDetailView(DetailView):
    model = Order
    template_name = "omsapp/order_detail.html"
    
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