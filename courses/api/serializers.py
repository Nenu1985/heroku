from rest_framework import serializers
from ..models import Subject


# serializer for the Subject model. Serializers are defined in a similar
# fashion to Django 's Form and ModelForm classes
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject

        fields = ['id', 'title', 'slug']
