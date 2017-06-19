

from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
#from book_lovers.forms import CreateForm

from .models import Book
#from .forms import BookCreateForm, BookUpdateForm
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
    form_class = BookCreateForm


class BooksUpdateView(LoginRequiredMixin, BooksActionMixin, UpdateView):
    model = Book
    success_msg = "Book updated!"
    form_class = BookUpdateForm


class BooksDetailView(DetailView):
    model = Book

class BooksListView(ListView):
    model = Book
    context_object_name = 'Book'

    def book_list(self):
        return Book.objects.all()

    # def let_us_create(request):
    #     if request.method == 'GET':
    #         form = CreateForm(request.GET)
    #         return HttpResponseRedirect('books:create')
