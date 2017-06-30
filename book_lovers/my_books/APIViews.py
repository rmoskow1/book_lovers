from rest_framework.views import APIView  #a way to make normal views return API data

from rest_framework import viewsets,generics, permissions
from .serializers import BookSerializer, PublisherSerializer,AuthorSerializer, UserSerializer
from django.db.models import Count
from django.contrib.auth.models import User
from .models import Book, Author, Publisher
import django_filters.rest_framework



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
    #@detail_route(methods = ['patch'])
    #def partial_update(self, request, *args, **kwargs):
        #instance = self.queryset.get(pk=kwargs.get('pk'))
        #serializer = self.serializer_class(instance, data=request.data, partial=True)
        #serializer.is_valid(raise_exception=True)
        #serializer.save()
        #return Response(serializer.data
    def patch(self, request,id):
        testmodel = self.get_object(id)
        serializer = BookSerializer(testmodel, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return JsonReponse(code=201, data=serializer.data)
        return JsonResponse(code=400, data="wrong parameters")   

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
    
    #queryset = Book.objects.filter(users_who_favorite__gte=1).distinct()
    num_fans = 1
    queryset = Book.objects.annotate(users=Count('users_who_favorite')).filter(users__gte=num_fans) #filter out the books with num_fans users 
    serializer_class = BookSerializer
    
class BookList2(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

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
