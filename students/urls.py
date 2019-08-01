from django.urls import path
from students import views

app_name = 'students'

urlpatterns = [
    path('register/',
         views.StudentRegistrationView.as_view(),
         name='students-registration'),
   path('enroll-course/',
        views.StudentEnrollCourseView.as_view(),
        name='student-enroll-course'),
]
