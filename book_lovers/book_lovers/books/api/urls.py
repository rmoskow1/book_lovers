from rest_framework import routers
from book_lovers.books.api import views


router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'popular-books', views.PopularBookViewSet)
router.register(r'publishers', views.PublisherViewSet)

urlpatterns = [

]
urlpatterns += router.urls
