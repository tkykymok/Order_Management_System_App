from django.urls import path
from . import views


urlpatterns = [
    path('', views.MenuView.as_view(), name='menu'),
    path('order-entry/', views.OrderCreateView.as_view(), name='order_entry'),
    path('order-number-create/', views.OrderNumberCreateView.as_view(), name='order_number_create'),
    path('item-info-get/', views.ItemInfoGetView.as_view(), name='item_info_get'),
    
    
    
    # path('update/<str:pk>/', views.OrderUpdateView.as_view(), name='update'),
    # path('success/', views.SuccessView.as_view(), name='success'),
    
    path('order-list/', views.OrderListView.as_view(), name='order_list'),
    # path('order-detail/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
]