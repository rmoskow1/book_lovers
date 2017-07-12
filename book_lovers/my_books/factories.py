from .models import Book, Publisher, Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import factory
import factory.fuzzy
import datetime
import random


class PublisherFactory(factory.DjangoModelFactory):
    class Meta:
        model = Publisher
        abstract = False

    name = factory.fuzzy.FuzzyText()
    address = factory.fuzzy.FuzzyText()
    city = factory.fuzzy.FuzzyText()
  
  
    
class ProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = Profile 
        abstract = False
    publisher = factory.SubFactory(PublisherFactory)    
    # We pass in profile=None to prevent UserFactory from creating another profile
    # (this disables the RelatedFactory)
    user = factory.SubFactory("my_books.factories.UserFactory", profile=None)


    
class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model= User
    username = factory.fuzzy.FuzzyText()
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.username)
    password = factory.fuzzy.FuzzyText()
     # We pass in 'user' to link the generated Profile to our just-generated User
    # This will call ProfileFactory(user=our_new_user), thus skipping the SubFactory.
    profile = factory.RelatedFactory("my_books.factories.ProfileFactory", 'user')
    is_staff = False


    '''@classmethod
    def with_fav_books(cls, numberOfBooks=4, *args, **kwargs):
        User = cls.create(*args, **kwargs)
        fav_books = BookFactory.create_batch(numberOfBooks, users_who_favorite = (User,))
        User.fav_books = fav_books

        return User'''
    


class BookFactory(factory.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.fuzzy.FuzzyText()
    publisher = factory.SubFactory(PublisherFactory)  # if it's one to many
    date = factory.fuzzy.FuzzyDate(datetime.date(2008, 1, 1))
    pen_name = factory.fuzzy.FuzzyText()
    uploader = factory.SubFactory(UserFactory)
    author = factory.SubFactory(UserFactory)
    isPublished = False
    isVerified = False  # default creation of a book

    '''@classmethod
    def users_who_favorite(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for user in extracted:
                self.users_who_favorite.add(user)'''