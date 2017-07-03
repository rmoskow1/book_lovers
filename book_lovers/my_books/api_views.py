from django.http import JsonResponse
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


#class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    #queryset = Book.objects.all()
    #serializer_class = BookSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

#display only the books with at least 2 users who favorite
class PopularBookViewSet(viewsets.ModelViewSet):

    #queryset = Book.objects.filter(users_who_favorite__gte=1).distinct()
    num_fans = 1
    queryset = Book.objects.annotate(users=Count('users_who_favorite')).filter(users__gte=num_fans) #filter out the books with num_fans users 
    serializer_class = BookSerializer

#identical to BookListView - but using generic views instead    
class BookList2(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

#a permission designed for UserViewSet -- only staff can see a list of all users. And only staff or the user itself can view a user detail page   
class IsStaffOrTargetUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow user to list all users if logged in user is staff
        return view.action == 'retrieve' or request.user.is_staff 
 
    def has_object_permission(self, request, view, obj):
        # allow logged in user to view own details, allows staff to view all records
        return request.user.is_staff or obj == request.user


class UserViewSet(viewsets.ModelViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsStaffOrTargetUser,)
    

class AuthorViewSet(viewsets.ModelViewSet): #author list - authors can be created here
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class PublisherViewSet(viewsets.ModelViewSet): #publisher list - publishers can be created here
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


#class PubDetailView(generics.RetrieveUpdateDestroyAPIView): #edit individual publishers
    #queryset = Publisher.objects.all()
    #serializer_class = PublisherSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
