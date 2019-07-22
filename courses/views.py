from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Course
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet


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

class CourseModuleUpdateView(TemplateResponseMixin, View):
    """
    handles the formset to add, update, and
    delete modules for a specific course
    """
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        """
        define this method to avoid repeating the code to build the formset
        :param data:
        :return:
        """
        return ModuleFormSet(instance=self.course,
                             data=data)

    def dispatch(self, request, pk):  # send
        """
        This method is provided by the View class. It takes
an HTTP request and its parameters and attempts to
delegate to a lowercase method that matches the HTTP
method used: a GET request is delegated to the get() method
and a POST request to post(), respectively. In this method, we
use the get_object_or_404() shortcut function to get the Course
object for the given id parameter that belongs to the current
user. We include this code in the dispatch() method because
we need to retrieve the course for both GET and POST requests.
We save it into the course attribute of the view to make it
accessible to other methods
        :param request:
        :param pk:
        :return:
        """
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        owner=request.user)
        return super(CourseModuleUpdateView,
                     self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        """
        We build an empty
ModuleFormSet formset and render it to the template together
with the current Course object using the render_to_response()
method provided by TemplateResponseMixin
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        """
        1. We build a ModuleFormSet instance using the submitted data.
        2. We execute the is_valid() method of the formset to
        validate all of its forms.
        3. If the formset is valid, we save it by calling the save()
        method. At this point, any changes made, such as
        adding, updating, or marking modules for deletion, are
        applied to the database. Then, we redirect users to the
        manage_course_list URL. If the formset is not valid, we
        render the template to display any errors, instead
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        formset = self.get_formset(data=request.POST)

        if formset.is_valid():
            formset.save()
            return redirect('courses:manage-course-list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})
