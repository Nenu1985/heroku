from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Course
from django.contrib.auth.mixins import LoginRequiredMixin, \
PermissionRequiredMixin

# Create your views here.

class OwnerMixin(object):
    """
    mixin will override the method that is used by the views
    to get the base QuerySet to filter objects by the
    owner attribute to retrieve objects that belong to
    the current user.
    Can be used for views tha interact with any model that
    contains an owner attribute.
    """
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    # form_valid() is saving the instance of views with forms
    # or modelforms (CreateView, UpdateView) and redirecting
    # the user to 'success_url'. We override this method to
    # automatically set the current user in the owner attribute
    # of the object being saved.
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('courses:manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    # The fields of the model to build the model form of the
    # CreateView and UpdateView views
    fields = ['subject', 'title', 'slug', 'overview']
    # Used by CreateView and UpdateView to redirect the user
    # after the form is successfully submitted
    success_url = reverse_lazy('courses:manage_course_list')
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    """
    Lists the courses created by the user
    """
    template_name = 'courses/manage/course/list.html'


class CourseCreateView(PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       CreateView):
    """
    Uses a modelform to create a new Course object
    """
    permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       UpdateView):
    """
    Allows editing an existing Course object
    """
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin,
                       OwnerCourseMixin,
                       DeleteView):
    """
    Defines success_url to redirect the user after the
    object is deleted
    """
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('courses:manage_course_list')
    permission_required = 'courses.delete_course'

# class ManageCourseListView(ListView):
#     model = Course
#     template_name = 'courses/manage/course/list.html'
#
#     def get_queryset(self):
#         qs = super(ManageCourseListView, self).get_queryset()
#         return qs.filter(owner=self.request.user)
