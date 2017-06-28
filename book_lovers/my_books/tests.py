# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, mock
from my_books.models import Book, Publisher, Author
import datetime
from django.contrib.auth.models import AnonymousUser, User
from my_books.views import FavoritesListView

# Create your tests here.
# class TestCaseMixin(TestCase):
#     def setUp(self):
#         grrr = Publisher.objects.create(name='How to Save a Life')
#         felix = Author.objects.create(name='Fix It Felix Jr.')
#         steve = Author.objects.create(name='Armless Steve')
#         AuthList = [felix,steve]
#         aa = Book.objects.create(title="Bob the Builder's Magical Mushrooms")
#         bb = Book.objects.create(title="Factory Mishaps and Other Ways to Lose a Limb", publisher=grrr, date='1955-11-12')
#         #aa.save()
#         #bb.save()
#         aa.author.add(AuthList[0])
#         aa.author.add(AuthList[1])
#         bb.author.add(AuthList[1])
#         self.user = User.objects.create_user(
#             username='pin', email='pin@pin.pin', password='pin-number')

def mocked_requests_get(books):

    #
    # felix = Author.objects.create(name='Fix It Felix Jr.')
    # steve = Author.objects.create(name='Armless Steve')
    # aa = Book.objects.create(id=1, title="Bob the Builder's Magical Mushrooms", author = (felix,))
    # bb = Book.objects.create(id=2, title="Factory Mishaps and Other Ways to Lose a Limb", author = (steve,))
    #
    #

    return {books}

    # class MockResponse:
    #     def __init__(self, json_data, status_code):
    #         self.json_data = json_data
    #         self.status_code = status_code
    #
    #     def json(self):
    #         return self.json_data
    #
    # if args[0] == 'http://someurl.com/test.json':
    #     return MockResponse({"key1": "value1"}, 200)
    # elif args[0] == 'http://someotherurl.com/anothertest.json':
    #     return MockResponse({"key2": "value2"}, 200)

# class BookCreateTest(TestCaseMixin):
#
#     def test_create_book(self):
#         aa = Book.objects.get(title="Bob the Builder's Magical Mushrooms")
#         bb = Book.objects.get(title="Factory Mishaps and Other Ways to Lose a Limb")
#
#         self.assertEqual(aa.date, None)
#         self.assertEqual(bb.date, datetime.date(1955, 11, 12))
#         self.assertEqual(len(Book.objects.all()), 2)
#
#
#     def test_delete_book(self):
#         Book.objects.get(title="Bob the Builder's Magical Mushrooms").delete()
#         self.assertEqual(len(Book.objects.all()), 1)


class FavoriteListViewTest(TestCase, FavoritesListView):
    def setUp(self):

        felix = Author.objects.create(name='Fix It Felix Jr.')
        steve = Author.objects.create(name='Armless Steve')
        AuthList = [felix, steve]
        aa = Book.objects.create(title="Bob the Builder's Magical Mushrooms")
        bb = Book.objects.create(title="Factory Mishaps and Other Ways to Lose a Limb")
        aa.save()
        bb.save()
        aa.author.add(AuthList[0])
        aa.author.add(AuthList[1])
        bb.author.add(AuthList[1])

        global myBooks
        myBooks = [aa,bb]

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_favorite(self, mockget):
        aa = Book.objects.get(title="Bob the Builder's Magical Mushrooms")
        bb = Book.objects.get(title="Factory Mishaps and Other Ways to Lose a Limb")
        aa.save()
        bb.save()

        user = User(id=1, username="a", password="b", email='c@d.efg')
        user.save()

        user.fav_books.add(aa)
        myView = FavoritesListView()
        myView.request = mockget.requests.get
        myView.request.user = user

        for book in myView.get_queryset():
            self.assertIn(book, user.fav_books.all())
        self.assertEqual(len(myView.get_queryset()), len(user.fav_books.all()))

