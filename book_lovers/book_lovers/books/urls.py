from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from book_lovers.books import views

urlpatterns = [
    url(r'^$', views.BooksListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', views.BooksDetailView.as_view(), name='detail'),
    url(r'^create/$', views.BooksCreateView.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)/$', views.BooksUpdateView.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', views.BooksDeleteView.as_view(), name='delete'),
    url(r'^favorites/$', views.FavoritesListView.as_view(), name='favorites'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='registration/login.html')),
    url(r'^logout/$', auth_views.logout, {"next_page": 'books:list'}, name='logout'),
]


# from django.conf.urls import url
# from rest_framework import routers
# from rest_framework_swagger.views import get_swagger_view
#
# from book_lovers.my_books import api_views
#
# schema_view = get_swagger_view(title='Pastebin API')
#
# router = routers.DefaultRouter()
# router.register(r'^', api_views.BookViewSet)
# router.register(r'popularbooks', api_views.PopularBookViewSet)
# router.register(r'publishers', api_views.PublisherViewSet)
# router.register(r'users', api_views.UserViewSet)
# router.register(r'profiles', api_views.ProfileViewSet)
#
#
# urlpatterns = [
#                 url(r'^docs/', schema_view),
#                 url(r'books2/', api_views.BookList2.as_view()),
# ]
#
# urlpatterns += router.urls






# from django.conf.urls import url
# from django.contrib.auth import views as auth_views
#
# from book_lovers.my_books import views
#
# urlpatterns = [
#     url(r'^$', views.BooksListView.as_view(), name='list'),
#     url(r'^(?P<pk>\d+)/$', views.BooksDetailView.as_view(), name='detail'),
#     url(r'^create/$', views.BooksCreateView.as_view(), name='create'),
#     url(r'^update/(?P<pk>\d+)/$', views.BooksUpdateView.as_view(), name='update'),
#     url(r'^delete/(?P<pk>\d+)/$', views.BooksDeleteView.as_view(), name='delete'),
#     url(r'^favorites/$', views.FavoritesListView.as_view(), name='favorites'),
#     url(r'^login/$', auth_views.LoginView.as_view(template_name='registration/login.html')),
#     url(r'^logout/$', auth_views.logout, {"next_page": 'books:list'}, name='logout'),
#
# ]