from django.conf.urls import url, include
from my_books import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$',views.BooksListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', views.BooksDetailView.as_view(), name='detail'),
    url(r'^create/$', views.BooksCreateView.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)/$', views.BooksUpdateView.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', views.BooksDeleteView.as_view(), name='delete'),
    url(r'^author/$', views.AuthorsCreateView.as_view(), name='author'),
<<<<<<< HEAD
    url(r'^favorites/$',views.FavoritesListView.as_view(),name = 'favorites'),
    url(r'^favorites_update/(?P<pk>\d+)/$',views.fav_updateView,name = 'favorites_update'),
=======
    url(r'^login/$', auth_views.LoginView.as_view(template_name='registration/login.html')),
    #url(r'^logout/$', auth_views.LogoutView.as_view(template_name='registration/logout.html'))

>>>>>>> 46accbc031959ec953d063c454decd0d4150b4ee
]