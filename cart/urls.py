from django.urls import path
from . import views

app_name = 'cart'  # Для темплейтов и конкретизации урла по имени апп

urlpatterns = [
    path('', views.cart_detail, name='cart-detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart-add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart-remove'),
]
