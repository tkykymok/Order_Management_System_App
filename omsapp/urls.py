from django.urls import path
from . import views


urlpatterns = [
    path('', views.MenuView.as_view(), name='menu'),
    path('order-entry/', views.OrderEntryView.as_view(), name='order_entry'),
    path('prj-code-get/', views.PrjCodeGet.as_view(), name='prj_code_get'),
    path('order-number-create/', views.OrderNumberCreate.as_view(), name='order_number_create'),
    path('item-info-get/', views.ItemInfoGet.as_view(), name='item_info_get'),
    path('order-confirm-create/', views.OrderCreateConfirm.as_view(), name='order_create_confirm'),
    path('order-info/', views.OrderInfoView.as_view(), name='order_info'),
    path('order-update/<str:id>/', views.OrderUpdate.as_view(), name='order_update'),
    path('order-delete/', views.OrderDelete.as_view(), name='order_delete'),
    
    path('shipment-entry/', views.ShipmentEntryView.as_view(), name='shipment_entry'),
    path('shipment-data-get/', views.ShipmentDataGet.as_view(), name='shipment_data_get'),
    path('shipment-complete/', views.ShipmentComplete.as_view(), name='shipment_complete'),
    
    
   
    # path('update/<str:pk>/', views.OrderUpdateView.as_view(), name='update'),
    # path('success/', views.SuccessView.as_view(), name='success'),
    
    # path('order-detail/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
]