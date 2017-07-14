from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView
from django.urls import reverse
from .models import Book
from django.db.models import Q










class FavoritesListView(BooksListView):
    # list of a user's favorite books
    def get_queryset(self):
        queryset = super(FavoritesListView, self).get_queryset()
        if self.request.user.is_authenticated():
            # return a filtered queryset
            return self.request.user.fav_books.all()
        # No q is specified so we return queryset
        return queryset


