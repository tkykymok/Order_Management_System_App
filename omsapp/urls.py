from django.urls import path
from . import views


urlpatterns = [
    path('', views.MenuView.as_view(), name='menu'),
    path('order-entry/', views.OrderCreateView.as_view(), name='order_entry'),
    path('prj-code-get/', views.PrjCodeGet.as_view(), name='prj_code_get'),
    path('order-number-create/', views.OrderNumberCreate.as_view(), name='order_number_create'),
    path('item-info-get/', views.ItemInfoGet.as_view(), name='item_info_get'),
    path('order-confirm-create/', views.OrderCreateConfirm.as_view(), name='order_create_confirm'),
    path('order-list/', views.OrderListView.as_view(), name='order_list'),
    path('order-update/<str:id>/', views.OrderUpdate.as_view(), name='order_update'),
    
    
    
    
    # path('update/<str:pk>/', views.OrderUpdateView.as_view(), name='update'),
    # path('success/', views.SuccessView.as_view(), name='success'),
    
    # path('order-detail/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
]