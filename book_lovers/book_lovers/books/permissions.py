from rest_framework import permissions

class BookViewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow user to list all users if logged in user is staff
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated():

            if request.method in permissions.SAFE_METHODS:

                if (obj.is_public()) \
                        or request.user.is_staff \
                        or ((request.user.profile.publisher == obj.publisher)
                            or (obj in request.user.uploaded_books.all())
                            or (obj in request.user.authored_books.all())):
                    return True
                else:
                    return False
            else:  # editing permissions
                if obj.is_public():
                    if request.user.is_staff:
                        return True

                else:
                    if request.user.is_staff \
                            or ((request.user.profile.publisher == obj.publisher)
                                or (obj in request.user.uploaded_books.all())
                                or (obj in request.user.authored_books.all())):
                        return True

        return False
