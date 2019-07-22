from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module

# a small abstraction on top of formsets that simplify working with
# related objects. This function allows us to build a model formset
# dynamically for the Module objects related to a Course object
ModuleFormSet = inlineformset_factory(Course,
                                      Module,
                                      fields=['title',  # The fields that will be included in each
                                              'description'],  # form of the formset
                                      extra=2,  # number of empty extra forms to
                                      # display in the formset
                                      can_delete=True)  # Boolean field for each form
# that will be rendered as a checkbox input.
# It allows you to mark the objects you want to delete
