from django.conf.urls import url
from my_books import views

urlpatterns = [
    url(r'^$',views.BooksListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', views.BooksDetailView.as_view(), name='detail'),
    url(r'^create/$', views.BooksCreateView.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)/$', views.BooksUpdateView.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', views.BooksDeleteView.as_view(), name='delete'),
    url(r'^author/$', views.AuthorsCreateView.as_view(), name='author'),
    url(r'^favorites/$',views.FavoritesListView.as_view(),name = 'favorites'),
    url(r'^favorites_update/(?P<pk>\d+)/$',views.fav_updateView,name = 'favorites_update'),
]