from django.db import models
from django.conf import settings


class Book(models.Model):

    title = models.CharField(max_length= 100)

    pen_name = models.CharField(max_length=100, verbose_name='author name', default = 'Insert Pen Name')

    publisher = models.ForeignKey('Publisher', null=True,blank = True)  # allows for unknown publisher

    date = models.DateField(blank=True, null=True)  # allows for unknown publishing date

    text = models.TextField(null=True, blank=True)

    #instead of changing the user model, do this. Books can access the users who have favorited them, by Book.users_who_favorite. And Users can access all of the books they have favorited, by user.fav_books
    users_who_favorite = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name = 'fav_books')

    isPublished = models.BooleanField(default=False)

    isVerified = models.BooleanField(default=False)

    tags = models.ManyToManyField('Tag',related_name = 'tagged_books', blank = True)

    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,blank = True, related_name='uploaded_books')

    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank = True, related_name='authored_books')

    def __str__(self):
        return self.title

    def is_public(self):
        if self.isPublished and self.isVerified:
            return True
        return False



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
    publisher = models.ForeignKey('Publisher', null=True, blank=True)

    def __str__(self):
        return self.user.__str__() + "'s profile"
