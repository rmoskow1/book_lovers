from __future__ import unicode_literals

from .api_views import BookViewPermission,BookViewSet
from my_books.models import Profile,Book,Publisher,Author
from django.contrib.auth.models import User,AnonymousUser
from django.test import TestCase,mock


class BookViewPermissionTest(TestCase, BookViewPermission):

    def setUp(self):
        author = Author.objects.create(name='Author')
        publisher = Publisher.objects.create(name='Apress')
        pub = Publisher.objects.create(name='Irrelevant')

        pu = Book.objects.create(title="Published", publisher=pub ,isPublished=True)
        up = Book.objects.create(title="Unpublished", publisher=publisher, isPublished=False)
        pu.save()
        up.save()
        pu.author.add(author)
        up.author.add(author)

    @mock.patch('requests.get')
    def test_permissions(self,mockget):
        pu = Book.objects.get(title="Published")
        up = Book.objects.get(title="Unpublished")
        pu.save()
        up.save()

        user1 = User(id=1, username="a", password="A", email='A@a.com')
        user2 = User(id=2, username="b", password="B", email='B@b.com')
        user3 = User(id=3, username="c", password="C", email='C@c.com')
        user4 = AnonymousUser()
        user1.save()
        user2.save()
        user3.save()

        profile1 = Profile.objects.create(user=user1, publisher=pu.publisher)
        profile2 = Profile.objects.create(user=user2, publisher=up.publisher)
        profile3 = Profile.objects.create(user=user3, publisher=pu.publisher)

        user1.owned_books.add(pu)
        user3.owned_books.add(up)

        myView = BookViewSet
        myView.request = mockget.requests.get

        # TEST 1: test if the user can access the Book list page
        # TEST 2: test if the user can access Book 1
        # TEST 3: test if the user can access Book 2

        myView.request.user = user1

        # yes - user is authenticated
        self.assertTrue(BookViewPermission.has_permission(myView.request, myView.request, myView))

        # yes - book is published
        self.assertTrue(BookViewPermission.has_object_permission(myView.request,myView.request,myView,pu))

        # no - book is unpublished, and user doesn't work for publisher or own the book
        self.assertFalse(BookViewPermission.has_object_permission(myView.request,myView.request,myView,up))

        myView.request.user = user2

        # yes - user is authenticated
        self.assertTrue(BookViewPermission.has_permission(myView.request, myView.request, myView))

        # yes - book is published
        self.assertTrue(BookViewPermission.has_object_permission(myView.request, myView.request, myView, pu))

        # yes - user works for the publisher
        self.assertTrue(BookViewPermission.has_object_permission(myView.request, myView.request, myView, up))

        myView.request.user = user3

        # yes - user is authenticated
        self.assertTrue(BookViewPermission.has_permission(myView.request, myView.request, myView))

        # yes - book is published
        self.assertTrue(BookViewPermission.has_object_permission(myView.request, myView.request, myView, pu))

        # yes - user owns the book
        self.assertTrue(BookViewPermission.has_object_permission(myView.request, myView.request, myView, up))

        myView.request.user = user4

        # NO to all - user is not authenticated
        self.assertFalse(BookViewPermission.has_permission(myView.request, myView.request, myView))
        self.assertFalse(BookViewPermission.has_object_permission(myView.request, myView.request, myView, pu))
        self.assertFalse(BookViewPermission.has_object_permission(myView.request, myView.request, myView, up))
