from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'books', include('book_lovers.books.api.urls')),
    url(r'users', include('book_lovers.users.api.urls')),
]