from django.urls import path
from . import views

app_name = 'collage'  # Для темплейтов и конкретизации урла по имени апп

urlpatterns = [

    # ex: /
    path('main/', views.main, name='main'),
    path('image/<int:img_id>/', views.show_image, name='show-image'),
    path('collage_form/', views.collage_input_form, name='collage-form'),
    path('delete-upload-async/', views.delete_upload_async, name='delete-upload-async'),

]