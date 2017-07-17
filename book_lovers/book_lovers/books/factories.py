from book_lovers.books.models import Book, Publisher
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
    uploader = factory.SubFactory(UserFactory)
    author = factory.SubFactory(UserFactory)
    isPublished = False
    isVerified = False  # default creation of a book has isPublished and isVerified both as false
