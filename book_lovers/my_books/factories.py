from .models import Book, Publisher, Author
from django.contrib.auth.models import User
import factory
import factory.fuzzy

# factories.py

class PublisherFactory(factory.DjangoModelFactory):
    class Meta:
        model = Publisher
        abstract = False
   
    name = factory.fuzzy.FuzzyText()
    address = factory.fuzzy.FuzzyText()
    city = factory.fuzzy.FuzzyText()

class BookFactory(factory.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.fuzzy.FuzzyText()
    publisher = factory.SubFactory(PublisherFactory) #if it's one to many
    date = factory.fuzzy.FuzzyDate()
    pen_name = factory.fuzzy.FuzzyText()
    uploader = factory.SubFactory(UserFactory)
    author = factory.SubFactory(UserFactory)
    uploader= factor.SubFactory(UserFactory)
    is_verified = False #default creation of a book
    def is_public(self):
        return False #this method is false by default
   
                
    @factory.post_generation
    def users_who_favorite(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for user in extracted:
                self.users_who_favorite.add(user) 
                

    
class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model= User
    username = factory.fuzzy.FuzzyText()
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.username)
    password = factory.fuzzy.FuzzyText()
    @factory.post_generation
    def fav_books(self, create, count, **kwargs):
        if count is None:
            count = 3

        fav_books = [BookFactory.create(users_who_favorite=(self,)) for i in range(count)]

        if not create:
            # Fiddle with django internals so self.product_set.all() works with build()
            self._prefetched_objects_cache = {'fav_book': fav_books}  

     
    