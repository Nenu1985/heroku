from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('create/',
         views.CourseCreateView.as_view(),
         name='course-create'),
    path('<pk>/edit/',
         views.CourseUpdateView.as_view(),
         name='course-edit'),
    path('<pk>/delete/',
         views.CourseDeleteView.as_view(),
         name='course-delete'),
    path('<pk>/module/',
         views.CourseModuleUpdateView.as_view(),
         name='course-module-update'),
    path('module/<int:module_id>/content/<model_name>/create/',
         views.ContentCreateUpdateView.as_view(),
         name='module-content-create'),
    path('module/<int:module_id>/content/<model_name>/<id>/',
         views.ContentCreateUpdateView.as_view(),
         name='module-content-update'),
    path('content/<int:id>/delete/',
         views.ContentDeleteView.as_view(),
         name='module-content-delete'),
    path('module/<int:module_id>/',
         views.ModuleContentListView.as_view(),
         name='module-content-list'),
    path('module/order/',
         views.ModuleOrderView.as_view(),
         name='module-order'),
    path('content/order/',
         views.ContentOrderView.as_view(),
         name='content-order'),
    path('subject/<slug:subject>/', views.CourseListView.as_view(),
         name='course-list-subject'),

    path('course/<slug:slug>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('',
         views.CourseListView.as_view(),
         name='course-list'),
]
