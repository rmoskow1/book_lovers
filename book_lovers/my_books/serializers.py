from rest_framework import serializers
from .models import Book,Author,Publisher,Tag
from django.contrib.auth.models import User
from django.db import models

class BookSerializer(serializers.ModelSerializer): #we'll be converting something to JSON based on the model
    owner = models.ForeignKey('auth.User', related_name='owned_books', on_delete = models.CASCADE)
    class Meta:
        model = Book
        #what attributes do we want to return to the user? Not necesarily everything...
        fields = ('title','author','publisher','owner')
        #everything: fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    owned_books = serializers.PrimaryKeyRelatedField(many = True, queryset = Book.objects.all())
    class Meta:
        model = User
        fields = ('username','password','email','owned_books')
        