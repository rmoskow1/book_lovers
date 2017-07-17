import factory
import factory.fuzzy
from django.contrib.auth.models import User
from book_lovers.books.factories import PublisherFactory
from .models import Profile


class ProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = Profile
        abstract = False
    publisher = factory.SubFactory(PublisherFactory)
    # We pass in profile=None to prevent UserFactory from creating another profile
    # (this disables the RelatedFactory)
    user = factory.SubFactory("book_lovers.users.factories.UserFactory", profile=None)


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.fuzzy.FuzzyText()
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.username)
    password = factory.fuzzy.FuzzyText()
    # We pass in 'user' to link the generated Profile to our just-generated User
    # This will call ProfileFactory(user=our_new_user), thus skipping the SubFactory.
    profile = factory.RelatedFactory("book_lovers.users.factories.ProfileFactory", 'user')
    is_staff = False
