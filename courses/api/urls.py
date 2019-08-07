from django.urls import path, include
from rest_framework import routers
from . import views

# create a DefaultRouter object and register our view set with the
# courses prefix
router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)


app_name = 'api'

urlpatterns = [
    path('subjects/',
         views.SubjectListView.as_view(),
         name='subject_list'),
    path('subjects/<pk>/',
         views.SubjectDetailView.as_view(),
         name='subject_detail'),
    path('courses/<pk>/enroll/',
         views.CourseEnrollView.as_view(),
         name='course-enroll'),
    path('', include(router.urls)),

]
