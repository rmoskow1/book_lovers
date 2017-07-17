from django.conf.urls import url, include
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    url(r'books/', include('book_lovers.books.api.urls')),
    url(r'users/', include('book_lovers.users.api.urls')),
    url(r'^docs/', get_swagger_view(title='Pastebin API')),
]