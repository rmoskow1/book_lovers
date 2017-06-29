from rest_framework import serializers
from .models import Book,Author,Publisher,Tag
from django.contrib.auth.models import User
from django.db import models


class UserSerializer(serializers.ModelSerializer):
    owned_books = serializers.PrimaryKeyRelatedField(many = True, queryset = Book.objects.all())
    class Meta:
        model = User
        fields = ('username','password','email','owned_books','fav_books')

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name',)

class BookSerializer(serializers.ModelSerializer): #we'll be converting something to JSON based on the model
    owner = models.ForeignKey('auth.User', related_name='owned_books', on_delete = models.CASCADE)
    author = AuthorSerializer(many=True, read_only=False)
    users_who_favorite =  serializers.StringRelatedField( read_only = False,many = True)
    
    class Meta:
        model = Book
        #what attributes do we want to return to the user? Not necesarily everything...
        fields = ('title','author','publisher','owner','users_who_favorite')
        #everything: fields = '__all__'
    
    def create(self, validated_data):
        #should be able to create new model instance for any related field
        users_data = validated_data.pop('users_who_favorite')
        book  = Book.objects.create(**validated_data)
        for users_data in users_data:
            User.objects.create(fav_books = (book,), **users_data)
        return books

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

