# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView

from .models import Book


class BooksActionMixin:
    fields = ['title', 'author', 'publisher', 'date']

    @property
    def success_msg(self):
        return NotImplemented


    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(BooksActionMixin, self).form_valid(form)


class BooksCreateView(LoginRequiredMixin, BooksActionMixin, CreateView):
    model = Book
    success_msg = "Book created!"


class BooksUpdateView(LoginRequiredMixin, BooksActionMixin, UpdateView):
    model = Book
    success_msg = "Book updated!"


class BooksDetailView(DetailView):
    model = Book
