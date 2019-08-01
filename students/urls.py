from django.urls import path
from students import views

app_name = 'students'

urlpatterns = [
    path('register/',
         views.StudentRegistrationView.as_view(),
         name='student-registration'),
    path('enroll-course/',
         views.StudentEnrollCourseView.as_view(),
         name='student-enroll-course'),
    path('courses/', views.StudentCourseListView.as_view(),
         name='student-course-list'),
    path('course/<pk>/',
         views.StudentCourseDetailView.as_view(),
         name='student-course-detail'),
    path('course/<pk>/<module_id>/',
         views.StudentCourseDetailView.as_view(),
         name='student-course-detail-module'),
]
