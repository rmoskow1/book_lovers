from book_lovers.books.models import Book, Publisher
from book_lovers.users.models import Profile
from django.contrib.auth.models import User
from book_lovers import users as user_factories
# from book_lovers.users.factories import UserFactory
# from book_lovers.users import factories
# import book_lovers.users.factories
# from book_lovers.users.factories import UserFactory
import book_lovers

import factory
import factory.fuzzy
import datetime


class PublisherFactory(factory.DjangoModelFactory):
    class Meta:
        model = Publisher
        abstract = False

    name = factory.fuzzy.FuzzyText()
    address = factory.fuzzy.FuzzyText()
    city = factory.fuzzy.FuzzyText()

# import statement here to avoid circular imports in books.api.tests
from book_lovers.users.factories import UserFactory


class BookFactory(factory.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.fuzzy.FuzzyText()
    publisher = factory.SubFactory(PublisherFactory)  # one to many
    date = factory.fuzzy.FuzzyDate(datetime.date(2008, 1, 1))
    pen_name = factory.fuzzy.FuzzyText()
    uploader = factory.SubFactory("book_lovers.users.factories.UserFactory")
    author = factory.SubFactory("book_lovers.users.factories.UserFactory")
    isPublished = False
    isVerified = False  # default creation of a book has isPublished and isVerified both as false
