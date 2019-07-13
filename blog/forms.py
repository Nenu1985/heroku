from django import forms
from .models import Comment, Post


class EmailPostFrom(forms.Form):
    # post's name
    name = forms.CharField(max_length=25)
    # sender email
    email = forms.EmailField()
    # receiver email
    to = forms.EmailField()
    # instead of input html widget, we gonna to use textarea:
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class SearchForm(forms.Form):
    query = forms.CharField()
