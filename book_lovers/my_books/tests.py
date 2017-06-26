# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import ListView
from my_books.views import BookSearchMixin
from django.test import TestCase, RequestFactory
from django.db.models import Q
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
        aa.author.add(AuthList[1])
        bb.author.add(AuthList[1])

        self.assertEqual(aa.author.get(name='Fix It Felix Jr.'), felix)

    def test_create_book(self):
        aa = Book.objects.get(title="Bob the Builder's Magical Mushrooms")
        bb = Book.objects.get(title="Factory Mishaps and Other Ways to Lose a Limb")

        self.assertEqual(aa.date, None)
        self.assertEqual(bb.date, datetime.date(1955, 11, 12))        
        self.assertEqual(len(Book.objects.all()), 2)


    def test_delete_book(self):
        Book.objects.get(title="Bob the Builder's Magical Mushrooms").delete()
        self.assertEqual(len(Book.objects.all()), 1)

        
class BookSearchMixinTest(TestCase):
    """based on dnmellen - tests mixin within a fake template"""
    class DummyView(BookSearchMixin, ListView):
        sacks = Author.objects.create(name = "Rabbi Lord Jonathan")
        pub =  Publisher.objects.create(name = "Apress", city = "Cedarhurst")
        book1 = Book.objects.create(title = "Harry Potato", publisher = pub )
        book1.author.add(sacks)
        elmo = Publisher.objects.create(name = "Elmo", address = "123")
        auth2 = Author.objects.create(name = "Pubby")
        book2 = Book.objects.create(title = "Booky", publisher = pub2)
        book2.author.add(auth2)
        book2.author.add(sacks)        
        template_name = "best_darn_template_eva.html" #needed to be defined for any TemplateView

    def setUp(self):
        super(BookSearchMixinTest,self).setUp
        self.View = self.DummyView()
        self.factory = RequestFactory()
        self.request
    
    def test_emptySearch(self):
        #if the request is empty, the search's queryset should be the same as the parents
        self.request = None 
        assertEqual(self.View.get_queryset(), self.get_queryset())
    def test_successSearch(self):
        #test - the resulting queryset should just be the view's queryset properly filtered
        request = self.factory.get("/list/")
        newQuery =  self.View.get_queryset.filter(Q(title__icontains=q)|Q(tags__name__iexact = q)|Q(author__name__icontains = q)).distinct()
        assertEqual(self.get_queryset(), newQuery)

