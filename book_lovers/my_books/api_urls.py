from rest_framework import routers
from my_books import api_views
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

router = routers.DefaultRouter()
router.register(r'books', api_views.BookViewSet) 
router.register(r'popularbooks', api_views.PopularBookViewSet)
router.register(r'publishers', api_views.PublisherViewSet)
router.register(r'users', api_views.UserViewSet)
router.register(r'profiles', api_views.ProfileViewSet)


urlpatterns = [
                url(r'^docs/', schema_view),
                url(r'books2/', api_views.BookList2.as_view()),
]

urlpatterns += router.urls
