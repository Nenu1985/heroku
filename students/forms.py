from django import forms
from courses.models import Course


# implement functionality for students to enroll in courses
class CourseEnrollForm(forms.Form):
    # we are not going to show this field to the user.We are going to use
    # this form in the CourseDetailView view to display a button to enroll
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)
