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
    path('order-update-data-get/', views.OrderUpdateDataGet.as_view(), name='order_update_data_get'),
    path('order-update-confirm/', views.OrderUpdateConfirm.as_view(), name='order_update_confirm'),
    path('order-delete-confirm/', views.OrderDeleteConfirm.as_view(), name='order_delete'),
    
    path('shipment-entry/', views.ShipmentEntryView.as_view(), name='shipment_entry'),
    path('shipment-data-get/', views.ShipmentDataGet.as_view(), name='shipment_data_get'),
    path('shipment-complete/', views.ShipmentComplete.as_view(), name='shipment_complete'),
    path('shipment-update-data-get/', views.ShipmentUpdateDataGet.as_view(), name='shipment_update_data_get'),
    path('shipment-update-confirm/', views.ShipmentUpdateConfirm.as_view(), name='shipment_update_confirm'),
    path('shipment-delete-confirm/', views.ShipmentDeleteConfirm.as_view(), name='shipment_delete_confirm'),
    path('shipment-info/', views.ShipmentInfoView.as_view(), name='shipment_info'),

    
    path('acceptance-entry/', views.AcceptanceEntryView.as_view(), name='acceptance_entry'),
    path('acceptance-data-get/', views.AcceptanceDataGet.as_view(), name='acceptance_data_get'),
    path('acceptance-complete/', views.AcceptanceComplete.as_view(), name='acceptance_complete'),
    path('acceptance-update-data-get/', views.AcceptanceUpdateDataGet.as_view(), name='acceptance_update_data_get'),
    path('acceptance-update-confirm/', views.AcceptanceUpdateConfirm.as_view(), name='acceptance_update_confirm'),
    path('acceptance-delete-confirm/', views.AcceptanceDeleteConfirm.as_view(), name='acceptance_delete_confirm'),
    path('acceptance-info/', views.AcceptanceInfoView.as_view(), name='acceptance_info'),
    
    
    path('item-info/', views.ItemInfoView.as_view(), name='item_info'),
    
    path('item-create/', views.ItemCreateView.as_view(), name='item_create'),
    path('item-update/', views.ItemUpdateView.as_view(), name='item_update'),

]