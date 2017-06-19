# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
#from book_lovers.forms import CreateForm

from .models import Book


class BooksActionMixin:
    fields = ['title', 'author', 'publisher', 'date', 'tags']

    @property
    def success_msg(self):
        return NotImplemented


    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(BooksActionMixin, self).form_valid(form)

class BooksCreateView(LoginRequiredMixin, BooksActionMixin, CreateView):
    model = Book
    success_msg = "Book created!"
    templlate_name_suffix = '_update_form'


class BooksUpdateView(LoginRequiredMixin, BooksActionMixin, UpdateView):
    model = Book
    success_msg = "Book updated!"


class BooksDetailView(DetailView):
    model = Book

class BooksListView(ListView):
    model = Book
    context_object_name = 'Book'

    def book_list(self):
        return Book.objects.all()
