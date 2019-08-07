from rest_framework import serializers
from ..models import Subject
from ..models import Course
from ..models import Module
from ..models import Content


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


# Relational fields are used to represent model relationships.
# They can be applied to ForeignKey, ManyToManyField and
# OneToOneField relationships, as well as to reverse relationships,
# and custom relationships such as GenericForeignKey
class ItemRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        """Override the RelatedField's method"""
        #  This method takes the target of the field as the
        #  value argument, and should return the representation
        #  that should be used to serialize the target.
        #  The value argument will typically be a model instance

        return value.render()


class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['order', 'item']


class ModuleWithContentsSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)

    class Meta:
        model = Module

        fields = ['order', 'title', 'description', 'contents']


class CourseWithContentsSerializer(serializers.ModelSerializer):
    modules = ModuleWithContentsSerializer(many=True)

    class Meta:
        model = Course

        fields = ['id', 'subject', 'title', 'slug',
              'overview', 'created', 'owner', 'modules']
