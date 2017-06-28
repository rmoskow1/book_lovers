from rest_framework import serializers
from .models import Book,Author,Publisher,Tag

class BookSerializer(serializers.ModelSerializer): #we'll be converting something to JSON based on the model
    
    class Meta:
        model = Book
        #what attributes do we want to return to the user? Not necesarily everything...
        fields = ('title','author','publisher')
        #everything: fields = '__all__'

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('name')
        