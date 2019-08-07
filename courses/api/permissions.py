from rest_framework.permissions import BasePermission


#
class IsEnrolled(BasePermission):
    # grant access to students enrolled to a course
    # return True to grand access or False otherwise.
    def has_object_permission(self, request, view, obj):
        """
        Override base method of BasePermissionClass

        Check that the user performing the request is present
        in the students relationship of the Course object (obj)
        """
        return obj.students.filter(id=request.user.id).exists()
