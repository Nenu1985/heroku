from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order-create'),
    path('admin/order/<int:order_id>/', views.admin_order_detail,
         name='admin-order-detail'),
    path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf,
         name='admin-order-pdf'),

]
