

from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
#from book_lovers.forms import CreateForm

from .models import Book
<<<<<<< HEAD


class BooksActionMixin(object):
=======
#from .forms import BookCreateForm, BookUpdateForm
class BooksActionMixin:
>>>>>>> b73db299ea7489a7ffca99e76fda0893413624e2
    fields = ['title', 'author', 'publisher', 'date', 'tags']

    @property
    def success_msg(self):
        return NotImplemented


    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(BooksActionMixin, self).form_valid(form)

class BooksCreateView(LoginRequiredMixin, BooksActionMixin, CreateView):
    model = Book
<<<<<<< HEAD
    success_msg = "Book created!"
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return redirect('books:list')
=======
    template_name_suffix = '_update_form'
    def get_success_url(self):
        return reverse('books:list')

>>>>>>> b73db299ea7489a7ffca99e76fda0893413624e2


class BooksUpdateView(LoginRequiredMixin, BooksActionMixin, UpdateView):
    model = Book
 
    def get_success_url(self):
        return reverse('books:detail',kwargs={'pk':self.object.pk})



class BooksDetailView(DetailView):
    model = Book

class BooksListView(ListView):
    model = Book
    context_object_name = 'Book'

    def book_list(self):
        return Book.objects.all()
