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


# from rest_framework import viewsets, generics, permissions
# from .serializers import BookSerializer, PublisherSerializer, UserSerializer, ProfileSerializer, BookAdminSerializer
# from django.db.models import Count
# from django.contrib.auth.models import User
# from book_lovers.books.models import Book, Publisher
# from django.db.models import Q
#
#
# class BookViewPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # allow user to list all users if logged in user is staff
#         return request.user.is_authenticated()
#
#     def has_object_permission(self, request, view, obj):
#         if request.user.is_authenticated():
#
#             if request.method in permissions.SAFE_METHODS:
#
#                 if (obj.is_public()) \
#                         or request.user.is_staff \
#                         or ((request.user.profile.publisher == obj.publisher)
#                             or (obj in request.user.uploaded_books.all())
#                             or (obj in request.user.authored_books.all())):
#                     return True
#                 else:
#                     return False
#             else:  # editing permissions
#                 if obj.is_public():
#                     if request.user.is_staff:
#                         return True
#
#                 else:
#                     if request.user.is_staff \
#                             or ((request.user.profile.publisher == obj.publisher)
#                                 or (obj in request.user.uploaded_books.all())
#                                 or (obj in request.user.authored_books.all())):
#                         return True
#
#         return False
#
#
# class BookViewSet(viewsets.ModelViewSet):
#     def get_queryset(self):
#         if self.request.user.is_staff:
#             return Book.objects.all()
#         else:
#             return Book.objects.filter(Q(isVerified=True, isPublished=True) | Q(uploader=self.request.user)
#                                        | Q(author=self.request.user) | Q(publisher=self.request.user.profile.publisher))
#
#     queryset = Book.objects.get_queryset()
#
#     filter_fields = ('isPublished', 'isVerified')
#     permission_classes = (BookViewPermission,)
#
#     def get_serializer_class(self):
#         # if the user is admin, use the BookAdminSerializer. For any other user, the base serializer
#         if self.request.user.is_staff:
#             return BookAdminSerializer
#         else:  # non-admin user
#             return BookSerializer
#
#     def perform_create(self, serializer):
#         data = self.request.data
#         post_type = data.__getitem__('type')
#         serializer.save(uploader=self.request.user)
#         if post_type == 'write':
#             serializer.save(author=self.request.user)
#         else:
#             serializer.save()
#
#
# # display only the books with at least 2 users who favorite
# class PopularBookViewSet(viewsets.ModelViewSet):
#     # queryset = Book.objects.filter(users_who_favorite__gte=1).distinct()
#     num_fans = 1
#     queryset = Book.objects.annotate(users=Count('users_who_favorite')
#                                      ).filter(users__gte=num_fans)  # filter out the books with num_fans users
#     serializer_class = BookSerializer
#
#
# # identical to BookListView - but using generic views instead
# class BookList2(generics.ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#
#
# # a permission designed for UserViewSet -- only staff can see a list of all users.
# # And only staff or the user itself can view a user detail page
# class IsStaffOrTargetUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # allow user to list all users if logged in user is staff
#         return view.action == 'retrieve' or request.user.is_staff
#
#     def has_object_permission(self, request, view, obj):
#         # allow logged in user to view own details, allows staff to view all records
#         return request.user.is_staff or obj == request.user
#
#
# class UserViewSet(viewsets.ModelViewSet):
#     model = User
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     permission_classes = (IsStaffOrTargetUser,)
#
#
# class PublisherViewSet(viewsets.ModelViewSet):  # publisher list - publishers can be created here
#     queryset = Publisher.objects.all()
#     serializer_class = PublisherSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#
# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
