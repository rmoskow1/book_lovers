from django.conf.urls import url, include
from django.contrib import admin
from API import urls



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^books/', include('book_lovers.books.urls', namespace='books')),
    url(r'^account/', include('django.contrib.auth.urls', namespace='account')),
   # url(r'^users/', include('book_lovers.users.urls', namespace='users')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(urls, namespace='api')),
]
