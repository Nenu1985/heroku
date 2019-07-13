from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

app_name = 'shop'

urlpatterns = [
    # post views
    path('', views.product_list, name='product-list'),
    path('<slug:category_slug>/', views.product_list,
         name='product-list-by-category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
         name='product-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
