from .models import Book, Publisher, Profile
from django.contrib.auth.models import User
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

