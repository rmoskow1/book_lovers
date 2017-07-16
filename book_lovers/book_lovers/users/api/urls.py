from django.conf.urls import url
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from book_lovers.users.api import views

schema_view = get_swagger_view(title='Pastebin API')

router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.ProfileViewSet)

urlpatterns = [
    url(r'^docs/', schema_view),
]
urlpatterns += router.urls
