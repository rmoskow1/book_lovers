from django.db import models
from django.contrib.auth.models import AbstractUser


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ManyToManyField('Author')  # one or more authors per book
    publisher = models.ForeignKey('Publisher', null=True)  # allows for unknown publisher
    date = models.DateField(blank=True, null=True)  # allows for unknown publishing date

    def _str_(self):
        return self.title


class Author(models.Model):
    # this class is being kept simple for this projects purposes. For other purposes, this field could be expanded to include other details
    name = models.Charfield(max_lenght=100)

    def _str_(self):
        return self.name


class Publisher(models.Model):
    # publisher name and location
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=60, blank=True)
    state_province = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=50, blank=True)

    def _str_(self):
        return self.name


class User(AbstractUser):
    favorites = models.ManyToMany('Books')
