from rest_framework.views import APIView  #a way to make normal views return API data
from rest_framework import viewsets,generics
from .serializers import BookSerializer
from rest_framework.response import Response

from django.contrib.auth.models import User
from .models import Book, Author

class BookList(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class =BookSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)    
    
class BookList2(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class UserList(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = None
