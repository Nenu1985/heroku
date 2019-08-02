from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Course
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet
from django.forms.models import modelform_factory
from django.apps import apps
from .models import Module, Content
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.db.models import Count
from .models import Subject
from django.views.generic.detail import DetailView

from students.forms import CourseEnrollForm


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
    success_url = reverse_lazy('courses:manage-course-list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    # The fields of the model to build the model form of the
    # CreateView and UpdateView views
    fields = ['subject', 'title', 'slug', 'overview']
    # Used by CreateView and UpdateView to redirect the user
    # after the form is successfully submitted
    success_url = reverse_lazy('courses:manage-course-list')
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

    def dispatch(self, request: object, pk: object) -> object:  # send
        """
        This method is provided by the View class. It takes
an HTTP request and its parameters and attempts to
delegate to a lowercase method that matches the HTTP
method used: a GET request is delegated to the get() method
# and a POST request to post(), respectively. In this method, we
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


class ContentCreateUpdateView(TemplateResponseMixin, View):
    """
    create and update contents of different models
    """
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        """
        - check that the given model name is one
        of the four content models: Text, Video, Image, or File;
        -  obtain the actual class for the given model name.
        """
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses',
                                  model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        """
         build a dynamic form using the modelform_factory()
         function of the form's framework
        :param model:
        :param args:
        :param kwargs:
        :return:
        """
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        """
        receives the following URL parameters and
        stores the corresponding module, model, and content object
        as class attributes
        :param module_id: The ID for the module that the content is/will be associated with
        :param model_name: The model name of the content to create/update
        :param id: The ID of the object that is being updated. It's None to create new objects
        """
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super(ContentCreateUpdateView,
                     self).dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)

        return self.render_to_response({'form': form,
                                        'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        """
        build themodelform passing any submitted data and files to it
        :param request:
        :param module_id:
        :param model_name:
        :param id:
        :return:
        """
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            # If no ID is provided, we know the user is creating a new
            # object instead of updating an existing one
            if not id:
                # new content
                Content.objects.create(module=self.module,
                                       item=obj)
            return redirect('courses:module-content-list', self.module.id)
        return self.render_to_response({'form': form,
                                        'object': self.obj})


class ContentDeleteView(View):
    """
    retrieves the Content object with the given ID;
    deletes the related Text, Video, Image, or File object;
    deletes the Content object and redirects the user to the
        module_content_list URL to list the other contents of the module
    """

    def post(self, request, id):
        content = get_object_or_404(Content,
                                    id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('courses:module-content-list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    """
    gets the Module object with the given ID that belongs to the
    current user and renders a template with the given module
    """
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)
        return self.render_to_response({'module': module})


# CsrfExemptMixin: To avoid checking the CSRF token in the POST
# requests. We need this to perform AJAX POST requests
# without having to generate a csrf_token.
# JsonRequestResponseMixin: Parses the request data as JSON and
# also serializes the response as JSON and returns an HTTP
# response with the application/json content type.
class ModuleOrderView(CsrfExemptMixin,
                      JsonRequestResponseMixin,
                      View):
    """orderss a course's modules"""

    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin,
                       JsonRequestResponseMixin,
                       View):
    """orders a module's contents"""

    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id,
                                   module__course__owner=request.user) \
                .update(order=order)
        return self.render_json_response({'saved': 'OK'})


class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        # retrieve all subjects, including the total number of
        # courses for each of them
        subjects = Subject.objects.annotate(
            total_courses=Count('courses'))

        # retrieve all available courses, includin:g the total number
        # of modules contained in each course
        courses = Course.objects.annotate(
            total_modules=Count('modules'))
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response({'subjects': subjects,
                                        'subject': subject,
                                        'courses': courses})


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView,
                        self).get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(
            initial={'course': self.object})  # current course object
        return context
