# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from my_books.models import Book, Publisher, Author
import datetime

# Create your tests here.
class BookTestCase(TestCase):
    def setUp(self):
        grrr = Publisher.objects.create(name='How to Save a Life')
        felix = Author.objects.create(name='Fix It Felix Jr.')
        steve = Author.objects.create(name='Armless Steve')
        AuthList = [felix,steve]
        aa = Book.objects.create(title="Bob the Builder's Magical Mushrooms")
        bb = Book.objects.create(title="Factory Mishaps and Other Ways to Lose a Limb", publisher=grrr, date='1955-11-12')
        #aa.save()
        #bb.save()
        aa.author.add(AuthList[0])
        bb.author.add(AuthList[1])

    def test_create_book(self):
        aa = Book.objects.get(title="Bob the Builder's Magical Mushrooms")
        bb = Book.objects.get(title="Factory Mishaps and Other Ways to Lose a Limb")

        self.assertEqual(aa.date, None)
        self.assertEqual(bb.date, datetime.date(1955, 11, 12))
        self.assertEqual(aa.author.all(), <)