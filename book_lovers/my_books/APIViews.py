from rest_framework.views import APIView  #a way to make normal views return API data
from rest_framework import viewsets
from .serializers import BookSerializer
from rest_framework.response import Response

from django.contrib.auth.models import User
from .models import Book, Author

class BookListTemp(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class =BookSerializer
