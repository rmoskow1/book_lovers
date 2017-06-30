from rest_framework.views import APIView  #a way to make normal views return API data

from rest_framework import viewsets,generics, permissions
from .serializers import BookSerializer, PublisherSerializer,AuthorSerializer, UserSerializer
from django.db.models import Count
from django.contrib.auth.models import User
from .models import Book, Author, Publisher
import django_filters.rest_framework


class BookList2(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class =BookSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


# class MultipleFieldLookupMixin(object):
#     """
#     Apply this mixin to any view or viewset to get multiple field filtering
#     based on a `lookup_fields` attribute, instead of the default single field filtering.
#     """
#     def get_object(self):
#         queryset = self.get_queryset()             # Get the base queryset
#         queryset = self.filter_queryset(queryset)  # Apply any filter backends
#         filter = {}
#         for field in self.lookup_fields:
#             if self.kwargs[field]: # Ignore empty fields.
#                 filter[field] = self.kwargs[field]
#         return filter  # Lookup the object







#display only the books with at least 2 users who favorite
class PopularBookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.filter(users_who_favorite__gte=1)
  
    serializer_class = BookSerializer
    


class BookList2(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly,)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly,)
    
    
class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)



#@api_view(['GET'])
#def api_root(request, format=None):
    #return Response({
        ##'users': reverse('user-list', request=request, format=format),
        #'books2': reverse('api:book-list', request=request, format=format)
    #})
