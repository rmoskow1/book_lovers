from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
#from book_lovers.forms import CreateForm

from .models import Book, Author



#class BooksActionMixin(object):

#from .forms import BookCreateForm, BookUpdateForm
class BooksActionMixin(object):
    fields = ['title', 'author', 'publisher', 'date', 'tags']

    @property
    def success_msg(self):
        return NotImplemented


    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(BooksActionMixin, self).form_valid(form)

class BooksCreateView(LoginRequiredMixin, BooksActionMixin, CreateView):
    model = Book

    # success_msg = "Book created!"
    # template_name_suffix = '_update_form'
    #
    # def get_success_url(self):
    #     return redirect('books:list')


    def get_success_url(self):
        return reverse('books:list')


class BooksUpdateView(LoginRequiredMixin, BooksActionMixin, UpdateView):
    model = Book

    template_name_suffix = '_update_form'
    def get_success_url(self):
        return reverse('books:detail',kwargs={'pk':self.object.pk})



class BooksDetailView(DetailView):
    model = Book

class BooksListView(ListView):
    model = Book
    context_object_name = 'Book'

    # def search(request):
    #     if request.method == 'GET':
    #         q = request.GET['q']
    #         books = Book.objects.filter(title__icontains=q)
    #         context['books'] = books


class BooksDeleteView(DeleteView):
    model = Book
    template_name_suffix = '_confirm_delete'

    def get_success_url(self):
        return reverse('books:list')

class AuthorsCreateView(CreateView):
    fields = ['name']
    model = Author

    def get_success_url(self):
        return reverse('books:create')

    # def form_valid(self, form):
    #     messages.info(self.request, self.success_msg)
    #     return super(BooksActionMixin, self).form_valid(form)

