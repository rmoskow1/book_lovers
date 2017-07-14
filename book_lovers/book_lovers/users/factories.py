from .models import Profile
from django.contrib.auth.models import User
import factory
import factory.fuzzy
from book_lovers.books.factories import PublisherFactory


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
        model = User
    username = factory.fuzzy.FuzzyText()
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.username)
    password = factory.fuzzy.FuzzyText()
    # We pass in 'user' to link the generated Profile to our just-generated User
    # This will call ProfileFactory(user=our_new_user), thus skipping the SubFactory.
    profile = factory.RelatedFactory("my_books.factories.ProfileFactory", 'user')
    is_staff = False
