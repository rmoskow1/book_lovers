from rest_framework import permissions


class BookViewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow user to list all books if logged in user is staff
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated():

            if request.method in permissions.SAFE_METHODS:  # not creating/updating/deleting a book
                # is book is public (isVerified and isPublished), or the user is admin, or the user is an uploader/
                # author/publisher then the book can be viewed
                if (obj.is_public()) \
                        or request.user.is_staff \
                        or ((request.user.profile.publisher == obj.publisher)
                            or (obj in request.user.uploaded_books.all())
                            or (obj in request.user.authored_books.all())):
                    return True
                else:
                    return False
            else:  # creating/updating/deleting a book
                # a public book can ONLY be edited by admin
                if obj.is_public():
                    if request.user.is_staff:
                        return True

                else:  # book is not public
                    if request.user.is_staff \
                            or ((request.user.profile.publisher == obj.publisher)
                                or (obj in request.user.uploaded_books.all())
                                or (obj in request.user.authored_books.all())):
                        return True

        return False
