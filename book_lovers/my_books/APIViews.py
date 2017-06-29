from rest_framework.views import APIView  #a way to make normal views return API data
from rest_framework import viewsets,generics,permissions
from .serializers import BookSerializer
from rest_framework.response import Response

from django.contrib.auth.models import User
from .models import Book, Author

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class =BookSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
class BookList2(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class User(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = None
    
    
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


#@api_view(['GET'])
#def api_root(request, format=None):
    #return Response({
        ##'users': reverse('user-list', request=request, format=format),
        #'books2': reverse('api:book-list', request=request, format=format)
    #})
