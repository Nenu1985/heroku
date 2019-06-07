# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from collage.models import Collage


# class PhotoForm(forms.ModelForm):
#     class Meta:
#         model = Photo

class InputUrlFrom(forms.Form):
    url_to_img = forms.CharField(label='Photo url', max_length=256);

# class CollageInputForm(forms.Form):
#     photo_num = forms.IntegerField()
#     photo_cols = forms.IntegerField()
#     photo_tag = forms.CharField(max_length=30)
#     sizes = PhotoSize.objects.all().order_by('size')
#     photo_size = forms.ModelChoiceField(queryset=sizes, empty_label=sizes.first(), to_field_name='size')
#     #photo_size = forms.IntegerField()


class CollageCreateForm(forms.ModelForm):
    class Meta:
        model = Collage
        fields = (
            'photo_number',
            'photo_size',
            'cols_number',
            'photo_tag',
        )
        # exclude = [
        #     'delivered',
        #     'date_created',
        #     'date_delivered',
        #     'delivery',
        # ]


