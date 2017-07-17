from django.db import models
from book_lovers.books.models import Publisher
from django.conf import settings


class Profile(models.Model):
    """User's can have a Publisher as a foreign key; a user is considered part of this publishing company"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    publisher = models.ForeignKey(Publisher, null=True, blank=True)

    def __str__(self):
        return self.user.__str__() + "'s profile"
