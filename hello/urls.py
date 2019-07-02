from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

app_name = 'hello'

urlpatterns = [
    # post views
    path('success_message/', views.success_message, name='success'),
    path('error_message/', views.error_message, name='error'),

    path("greetings", views.greetings, name="greetings"),
    path('vue-calc/', TemplateView.as_view(template_name='hello/vue_calc.html'),
         name='vue-calc')
]
