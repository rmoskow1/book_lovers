from rest_framework import serializers
from .models import Book,Author,Publisher,Tag
from django.contrib.auth.models import User
from django.db import models



class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer): #we'll be converting something to JSON based on the model
    owner = models.ForeignKey('auth.User', related_name='owned_books',  on_delete = models.CASCADE)
  #  author = AuthorSerializer(many=True, read_only=False)
    users_who_favorite =  serializers.StringRelatedField( read_only = True,many = True)
    
    class Meta:
        model = Book
        fields = ('id','title','author','publisher','owner','users_who_favorite')
        #everything: fields = '__all__'
    
    #def create(self, validated_data):
        ##should be able to create new model instance for any related field
        #users_data = validated_data.pop('users_who_favorite')
        #book  = Book.objects.create(**validated_data)
        #for users_data in users_data:
            #User.objects.create(fav_books = (book,), **users_data)
        #return book
    
class UserSerializer(serializers.ModelSerializer):
    #owned_books = serializers.PrimaryKeyRelatedField(many = True, queryset = Book.objects.all())
   # my_owned_books = BookSerializer(many = True, ) #Lists are not currently supported in HTML input. - from the form. Books are displayed in full. You have to enter data for books as full dictionaries, maybe creating a new one is fine?
    class Meta:
        model = User
        fields = ('username','email', 'owned_books', 'fav_books')
        write_only_fields = ('password')
        # extra_kwargs = {
        #     'owned_books':{'write_only':True},
        #     #'my_owned_books':{'write_only':True}
        #     }

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

