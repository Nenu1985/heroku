from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'pizzapp'

urlpatterns = [
    path('sign-in/', auth_views.LoginView.as_view(template_name='pizzashop/sign_in.html'),
         name='pizzashop-sign-in'),

    path('sign-out/', auth_views.LogoutView.as_view(),
         name='pizzashop-sign-out'),

    path('', views.pizzashop_home, name='home'),
    path('pizzapp/', views.pizzashop_home, name='pizzashop-home'),

    path('sign-up/', views.pizzashop_sign_up, name='pizzashop-sign-up'),

    path('account/', views.pizzashop_account, name='pizzashop-account'),
    path('pizza/', views.pizzashop_pizza, name='pizzashop-pizza'),
    path('pizza/add/', views.pizzashop_add_pizza, name='pizzashop-add-pizza'),
    path('pizza/edit/<pizza_id>/', views.pizzashop_edit_pizza, name='pizzashop-edit-pizza'),
]