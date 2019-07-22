from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('',
         views.ManageCourseListView.as_view(),
         name='manage-course-list'),
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
]
