from django.conf.urls import url
from my_books import views

urlpatterns = [
    url(r'^$',views.BooksListView.as_view()),
    url(r'^(?P<pk>\d+)/$', views.BooksDetailView.as_view(), name='detail'),
    #url(r'^$', views.BooksCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', views.BooksUpdateView.as_view(), name='update'),
]