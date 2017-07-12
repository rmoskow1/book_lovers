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
    
    #@classmethod
    #def _generate(cls, create, attrs):
        #"""Override the default _generate() to disable the post-save signal."""

        ## Note: If the signal was defined with a dispatch_uid, include that in both calls.
     ##   post_save.disconnect(handler_create_user_profile, auth_models.User)
        #user = super(UserFactory, cls)._generate(create, attrs)
      ##  post_save.connect(handler_create_user_profile, auth_models.User)
        #return user
    @classmethod
    def with_fav_books(cls, numberOfBooks=4, *args, **kwargs):
        User = cls.create(*args, **kwargs)
        fav_books = BookFactory.create_batch(numberOfBooks, users_who_favorite = (User,))
        User.fav_books = fav_books

        return User
    
    
    #def fav_books(self, create, count, **kwargs):
        #if count is None:
            #count = 2
      
        #fav_books = [BookFactory.create(users_who_favorite=(self,)) for i in range(count)]

        #if not create:
            ## Fiddle with django internals so self.product_set.all() works with build()
            #self._prefetched_objects_cache = {'fav_book': fav_books}  

class BookWithPkFactory(factory.DjangoModelFactory):
    class Meta:
        model = Book
    pk = random.randint(0,10)
    title = factory.fuzzy.FuzzyText()
    publisher = factory.SubFactory(PublisherFactory) #if it's one to many
    date = factory.fuzzy.FuzzyDate(datetime.date(2008, 1, 1))
    pen_name = factory.fuzzy.FuzzyText()
    uploader = factory.SubFactory(UserFactory)
    uploader = factory.SubFactory(UserFactory)
    author = factory.SubFactory(UserFactory)
    isPublished = False
    isVerified = False #default creation of a book



class ProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = Profile
    publisher = factory.SubFactory(PublisherFactory)

class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.fuzzy.FuzzyText()
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.username)
    password = factory.fuzzy.FuzzyText()
    log = factory.RelatedFactory(ProfileFactory, 'user')


        # @factory.post_generation
    # def fav_books(self, create, count, **kwargs):
    #     if count is None:
    #         count = 2
    #
    #     fav_books = [BookFactory.create(users_who_favorite=(self,)) for i in range(count)]
    #
    #     if not create:
    #         # Fiddle with django internals so self.product_set.all() works with build()
    #         self._prefetched_objects_cache = {'fav_book': fav_books}


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

    # def isPublic(self):
    #     return False  # this method is false by default

    @classmethod
    def users_who_favorite(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for user in extracted:
                self.users_who_favorite.add(user) 