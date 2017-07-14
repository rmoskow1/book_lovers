from rest_framework import serializers
from .models import Book, Publisher, Tag, Profile
from django.contrib.auth.models import User










class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'uploaded_books', 'authored_books', 'fav_books', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
            }
   
    def create(self, validated_data):
        # create a new user with a properly hashed password
        # using the default create would produce a user without an unhashed password
        user = super().create(validated_data)
        user.set_password(validated_data['password']) 
        user.save()
        return user





class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
