from rest_framework import routers
from my_books import APIViews
from django.conf.urls import url,include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

router = routers.DefaultRouter()
router.register(r'books', APIViews.BookViewSet) 
router.register(r'popularbooks', APIViews.PopularBookViewSet)
router.register(r'authors',APIViews.AuthorViewSet)
router.register(r'publishers', APIViews.PublisherViewSet)
router.register(r'users',APIViews.UserViewSet,'list')



urlpatterns = [
                url(r'^docs/', schema_view),
                url(r'books2/',APIViews.BookList2.as_view()),
]
urlpatterns += router.urls