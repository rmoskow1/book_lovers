from rest_framework import routers

from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from book_lovers.books.api import views
schema_view = get_swagger_view(title='Pastebin API')

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'popular-books', views.PopularBookViewSet)
router.register(r'publishers', views.PublisherViewSet)

urlpatterns = [
                url(r'^docs/', schema_view),
]
urlpatterns += router.urls
