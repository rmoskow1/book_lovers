from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView
from django.urls import reverse
from django.contrib.auth import logout, login
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
#from book_lovers.forms import CreateForm
from django.conf import settings

from .models import Book, Author
from django.db.models import Q


#class BooksActionMixin(object):

#class Favorites_updateView(DetailView):
    #model = Book
# def fav_updateView(request):
#     model = Book
#
#     if self.object in request.user.fav_books.all():
#         request.user.fav_books.all().remove(self.object)
#     else:
#         request.user.fav_books.all().add(self.object)
#     return render(request,request.PATH)
# def fav_form(self,request):
#     model = Book
#
#     if self.object in request.user.fav_books.all():
#         request.user.fav_books.all().remove(self.object)
#     else:
#         request.user.fav_books.all().add(self.object)
#     return HttpResponseRedirect(reverse('books:detail'))
           


#from .forms import BookCreateForm, BookUpdateForm
class BooksActionMixin(object):
    fields = ['title', 'author', 'publisher', 'date', 'tags']

    @property
    def success_msg(self):
        return NotImplemented


    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(BooksActionMixin, self).form_valid(form)
    
class TitleSearchMixin(object):
    def get_queryset(self):
# Fetch the queryset from the parent's get_queryset
        queryset = super(TitleSearchMixin, self).get_queryset()
# Get the q GET parameter
        q = self.request.GET.get('q')
        if q:
# return a filtered queryset
            return queryset.filter(Q(title__icontains=q)|Q(tags__name__iexact = q)|Q(author__name__icontains = q)).distinct()
# No q is specified so we return queryset
        return queryset

class BooksCreateView(LoginRequiredMixin, BooksActionMixin, CreateView):
    model = Book

    # success_msg = "Book created!"
    # template_name_suffix = '_update_form'
    #
    # def get_success_url(self):
    #     return redirect('books:list')
    login_url = 'account:login'


    def get_success_url(self):
        return reverse('books:list')

    # def get_context_data(self, *args, **kwargs):
    #
    #     import ipdb
    #     ipdb.set_trace()
    #     temp = super().get_context_data(*args, **kwargs)
    #     return temp

class BooksUpdateView(LoginRequiredMixin, BooksActionMixin, UpdateView):
    model = Book

    template_name_suffix = '_update_form'

    login_url = 'account:login'

    def get_success_url(self):
        return reverse('books:detail',kwargs={'pk':self.object.pk})



class BooksDetailView(DetailView, UpdateView):
    model = Book
    fields = ['users_who_favorite']
   # status = "Favorite" if model in self.request.User.fav_books.all() else "Unfavorite"
   # status = "Favorite" if model in self.request.User.fav_books.all() else "Unfavorite"
   #  def get_context_data(self, request):
   #          # Call the base implementation first to get a context
   #          context = super(self).get_context_data()
   #          # Add in a QuerySet of all the books
   #          context['status'] = "Favorite" if model not in request.User.fav_books.all() else "Unfavorite"
   #          return context


    template_name_suffix = '_detail'

    def get_success_url(self):
        return reverse('books:list')

    # def favorite_request(request):
    #         if request.method == 'GET':
    #             if object in request.user.fav_books.all():
    #                 request.user.fav_books.add(request.user)
    #             else:
    #                 request.user.fav_books.remove(request.user)

    def get_context_data(self, **kwargs):

        context = super(BooksDetailView, self).get_context_data(**kwargs)

        if self.object in self.request.user.fav_books.all():
            context['favorite'] = False
        else:
            context['favorite'] = True
        return context




class BooksListView(TitleSearchMixin,ListView):
    model = Book
    context_object_name = 'Book'



class FavoritesListView(BooksListView):
    def get_queryset(self):
        queryset = super(FavoritesListView, self).get_queryset()
        if self.request.user.is_authenticated():
        # return a filtered queryset
            return self.request.user.fav_books.all()
# No q is specified so we return queryset
        return queryset


class BooksDeleteView(LoginRequiredMixin, DeleteView):

    model = Book
    template_name_suffix = '_confirm_delete'

    login_url = 'account:login'

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



