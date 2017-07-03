from django.http import JsonResponse
from rest_framework.views import APIView  #a way to make normal views return API data

from rest_framework import viewsets,generics, permissions
from .serializers import BookSerializer, PublisherSerializer,AuthorSerializer, UserSerializer
from django.db.models import Count
from django.contrib.auth.models import User
from .models import Book, Author, Publisher
from django.http import Http404
import django_filters.rest_framework

from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class =BookSerializer
    filter_fields = ('title',)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


    def patch(self, request):
        data = request.data
        testmodel = (data.get('id'))
        serializer = BookSerializer(data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(code=201, data=serializer.data)
        return JsonResponse(code=400, data="wrong parameters")   

class BookViewPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated():
            if (not request.object.isPublished) and (request.user.profile.is_publisher() or request.user.profile.is_author()):
                return Http404
            else:
                return request.object


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = ('BookViewPermission',)

#display only the books with at least 2 users who favorite
class PopularBookViewSet(viewsets.ModelViewSet):

    #queryset = Book.objects.filter(users_who_favorite__gte=1).distinct()
    num_fans = 1
    queryset = Book.objects.annotate(users=Count('users_who_favorite')).filter(users__gte=num_fans) #filter out the books with num_fans users 
    serializer_class = BookSerializer
    
class BookList2(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
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
