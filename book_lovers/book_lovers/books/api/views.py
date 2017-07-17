from django.db.models import Count
from rest_framework import viewsets, permissions
from book_lovers.books.permissions import BookViewPermission
from book_lovers.books.models import Book, Publisher
from .serializers import BookSerializer, PublisherSerializer, BookAdminSerializer


class BookViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Book.objects.for_user(self.request.user)

    queryset = Book.objects.get_queryset()
    filter_fields = ('isPublished', 'isVerified')
    permission_classes = (BookViewPermission,)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return BookAdminSerializer
        else:  # non-admin user
            return BookSerializer

    def perform_create(self, serializer):
        data = self.request.data
        post_type = data['type']
        if post_type == 'write':
            serializer.save(author=self.request.user, uploader=self.request.user)
        elif post_type == 'upload':
            serializer.save(uploader=self.request.user)


class PopularBookViewSet(viewsets.ModelViewSet):
    """displays only the books with at least NUM_FANS users_who_favorite"""
    NUM_FANS = 1
    queryset = Book.objects.annotate(user_fans=Count('users_who_favorite')
                                     ).filter(user_fans__gte=NUM_FANS)  # filter out the books with num_fans users
    serializer_class = BookSerializer


class PublisherViewSet(viewsets.ModelViewSet):  # publisher list - publishers can be created here
    serializer_class = PublisherSerializer
    queryset = Publisher.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
