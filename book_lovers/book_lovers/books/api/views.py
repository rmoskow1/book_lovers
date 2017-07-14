from django.db.models import Count
from django.db.models import Q
from rest_framework import viewsets, permissions
from book_lovers.books.permissions import BookViewPermission
from book_lovers.books.models import Book, Publisher
from .serializers import BookSerializer, PublisherSerializer, BookAdminSerializer


class BookViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.request.user.is_staff:
            return Book.objects.all()
        else:
            return Book.objects.filter(Q(isVerified=True, isPublished=True) | Q(uploader=self.request.user)
                                       | Q(author=self.request.user) | Q(publisher=self.request.user.profile.publisher))

    queryset = Book.objects.get_queryset()

    filter_fields = ('isPublished', 'isVerified')
    permission_classes = (BookViewPermission,)

    def get_serializer_class(self):
        # if the user is admin, use the BookAdminSerializer. For any other user, the base serializer
        if self.request.user.is_staff:
            return BookAdminSerializer
        else:  # non-admin user
            return BookSerializer

    def perform_create(self, serializer):
        data = self.request.data
        post_type = data.__getitem__('type')
        serializer.save(uploader=self.request.user)
        if post_type == 'write':
            serializer.save(author=self.request.user)
        else:
            serializer.save()


# display only the books with at least 2 users who favorite
class PopularBookViewSet(viewsets.ModelViewSet):
    # queryset = Book.objects.filter(users_who_favorite__gte=1).distinct()
    num_fans = 1
    queryset = Book.objects.annotate(users=Count('users_who_favorite')
                                     ).filter(users__gte=num_fans)  # filter out the books with num_fans users
    serializer_class = BookSerializer


class PublisherViewSet(viewsets.ModelViewSet):  # publisher list - publishers can be created here
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


