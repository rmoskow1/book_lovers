from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView
from book_lovers.books.models import Book


class BooksActionMixin(object):
    fields = ['title', 'pen_name', 'publisher', 'date', 'tags', 'uploader', 'isVerified', 'isPublished']

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(BooksActionMixin, self).form_valid(form)


class BookSearchMixin(object):
    def get_queryset(self):
        # Fetch the queryset from the parent's get_queryset
        queryset = super(BookSearchMixin, self).get_queryset()
        # Get the q GET parameter
        q = self.request.GET.get('q')
        if q:
            # return a filtered queryset
            return queryset.filter(Q(title__icontains=q) | Q(tags__name__iexact=q)
                                   | Q(pen_name__icontains=q) | Q(publisher__name__icontains=q)
                                   | Q(uploader__name__icontains=q)).distinct()
        # No q is specified so we return queryset
        return queryset


class BooksCreateView(LoginRequiredMixin, BooksActionMixin, CreateView):
    model = Book
    login_url = 'account:login'

    def get_success_url(self):
        return reverse('books:list')


class BooksUpdateView(LoginRequiredMixin, BooksActionMixin, UpdateView):
    model = Book

    template_name_suffix = '_update_form'

    login_url = 'account:login'

    def get_success_url(self):
        return reverse('books:detail', kwargs={'pk': self.object.pk})


class BooksDeleteView(LoginRequiredMixin, DeleteView):

    model = Book
    template_name_suffix = '_confirm_delete'

    login_url = 'account:login'

    def get_success_url(self):
        return reverse('books:list')


class BooksDetailView(DetailView, UpdateView):
    model = Book
    fields = ['users_who_favorite']
    template_name_suffix = '_detail'

    def get_success_url(self):
        return reverse('books:list')

    def get_context_data(self, **kwargs):

        context = super(BooksDetailView, self).get_context_data(**kwargs)

        if self.object in self.request.user.fav_books.all():
            context['favorite'] = False
        else:
            context['favorite'] = True
        return context


class BooksListView(BookSearchMixin, ListView):
    # list of all public books in database

    context_object_name = 'Book'

    def get_queryset(self):
        return Book.objects.filter(isVerified=True)


class FavoritesListView(BooksListView):
    # list of a user's favorite books
    def get_queryset(self):
        queryset = super(FavoritesListView, self).get_queryset()
        if self.request.user.is_authenticated():
            # return a filtered queryset
            return self.request.user.fav_books.all()
        # No q is specified so we return queryset
        return queryset

