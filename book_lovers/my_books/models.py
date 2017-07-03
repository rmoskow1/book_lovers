from django.db import models
from django.conf import settings



class Book(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null = True, related_name = 'owned_books')
    title = models.CharField(max_length= 100)
    author = models.ManyToManyField('Author')  # one or more authors per book
    publisher = models.ForeignKey('Publisher', null=True)  # allows for unknown publisher
    date = models.DateField(blank=True, null=True)  # allows for unknown publishing date
    #instead of changing the user model, do this. Books can access the users who have favorited them, by Book.users_who_favorite. And Users can access all of the books they have favorited, by user.fav_books
    users_who_favorite = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'fav_books')
    isPublished = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag',related_name = 'tagged_books', blank = True)
    def __str__(self):
        return self.title


class Author(models.Model):
    # this class is being kept simple for this projects purposes. For other purposes, this field could be expanded to include other details
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    # publisher name and location
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=60, blank=True)
    state_province = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length = 50)
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    books = models.ManyToManyField('Book')
    publisher = ''