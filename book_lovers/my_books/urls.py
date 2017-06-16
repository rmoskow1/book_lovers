from django.conf.urls import url
from my_books import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.BooksDetailView, name='detail'),
    url(r'^$', views.BooksCreateView, name='create'),
    url(r'^(?P<pk>\d+)/$', views.BooksUpdateView, name='update'),
]