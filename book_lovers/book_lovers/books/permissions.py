from rest_framework import permissions


class BookViewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow user to list all books if logged in user is staff
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):

        # non-authenticated users can't view or modify data
        if not request.user.is_authenticated():
            return False

        # admins can always view and modify data
        if request.user.is_staff:
            return True

        # if user is authenticated but isn't an admin

        # if the request is to view the data
        if request.method in permissions.SAFE_METHODS:

            # if it's public, the user can view it
            if obj.is_public():
                return True

            # if it's not public, only the publisher, uploader, or author can view it
            elif (request.user.profile.publisher == obj.publisher) or (obj in request.user.uploaded_books.all()) or (obj in request.user.authored_books.all()):
                return True
            else:
                return False

        # if the request is to modify the data
        elif request.method not in permissions.SAFE_METHODS:

            # if it's public, the user cannot modify it
            if obj.is_public():
                return False

            # if it's not public, only the publisher, uploader, or author can modify it
            elif (request.user.profile.publisher == obj.publisher) or (obj in request.user.uploaded_books.all()) or (obj in request.user.authored_books.all()):
                return True
            else:
                return False



