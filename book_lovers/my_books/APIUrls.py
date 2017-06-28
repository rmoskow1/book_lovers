from rest_framework import routers
from my_books import APIViews
from django.conf.urls import url,include

router = routers.DefaultRouter()
router.register(r'books', APIViews.BookListTemp) 
 
urlpatterns = [
                url(r'^', include(router.urls)),
                url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                 
]
 