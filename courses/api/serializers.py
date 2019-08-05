from rest_framework import serializers
from ..models import Subject
from ..models import Course
from ..models import Module


# serializer for the Subject model. Serializers are defined in a similar
# fashion to Django 's Form and ModelForm classes
class SubjectSerializer(serializers.ModelSerializer):
    """
       Serializer for the Subject model
       """

    class Meta:
        model = Subject

        fields = ['id', 'title', 'slug']


class ModuleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Module model

    * to provide serialization as nested data in the CourseSerializer
    """

    class Meta:
        model = Module
        fields = ['order', 'title', 'description']


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model
    """

    # many = True is to indicate that we are serializing multiple objs
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview',
                  'created', 'owner', 'modules']
