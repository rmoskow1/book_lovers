from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^books/', include('book_lovers.my_books.urls', namespace='books')),
    url(r'^account/', include('django.contrib.auth.urls', namespace='account')),
   # url(r'^api/books', include('book_lovers.books.api.api_urls', namespace='api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
