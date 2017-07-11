from rest_framework import serializers
from .models import Book,Publisher,Tag,Profile
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import models


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer): #we'll be converting something to JSON based on the model

    owner = models.ForeignKey('auth.User', related_name='owned_books',  on_delete = models.CASCADE)
  #  author = AuthorSerializer(many=True, read_only=False)
    users_who_favorite =  serializers.StringRelatedField(read_only = True,many = True)
    tags = serializers.StringRelatedField(read_only = True, many = True)
    class Meta:
        model = Book
        fields = ('id','title','pen_name','date','publisher','text','uploader','author','users_who_favorite','tags','isVerified','isPublished')
        extra_kwargs = {
        'isVerified':{'write_only':True},
        'isPublished':{'write_only':True}
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email', 'uploaded_books', 'authored_books', 'fav_books','password')
        extra_kwargs = {
            'password': {'write_only':True}
            }
   
    def create(self, validated_data):
        #create a new user with a properly hashed password
        #using the default create would produce a user without an unhashed password
        user = super().create(validated_data)
        user.set_password(validated_data['password']) 
        user.save()
        return user




class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'