from rest_framework import routers
from my_books import api_views
from django.conf.urls import url,include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

router = routers.DefaultRouter()
router.register(r'publishers', api_views.PublisherViewSet)
router.register(r'books', api_views.BookViewSet)
router.register(r'popularbooks', api_views.PopularBookViewSet)
router.register(r'authors', api_views.AuthorViewSet)
router.register(r'users', api_views.UserViewSet)


urlpatterns = [
                url(r'^docs/', schema_view),
                url(r'bookdetail/(?P<pk>\d+)/$', api_views.BookDetailView.as_view()),
                url(r'books2/', api_views.BookList2.as_view()),
]
urlpatterns += router.urls