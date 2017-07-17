from rest_framework import routers
from book_lovers.users.api import views

router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.ProfileViewSet)

urlpatterns = [

]
urlpatterns += router.urls
