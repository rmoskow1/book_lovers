from django.http import JsonResponse
from rest_framework import viewsets,generics, permissions
from .serializers import BookSerializer, PublisherSerializer, UserSerializer, ProfileSerializer,  BookAdminSerializer
from django.db.models import Count
from django.contrib.auth.models import User
from .models import Book,Publisher, Profile
from django.http import Http404
import django_filters.rest_framework

from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.db.models import Q


class BookViewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow user to list all users if logged in user is staff
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated():
           
            if request.method in permissions.SAFE_METHODS:
 
                if (obj.is_public()) \
                        or request.user.is_staff\
                        or ((request.user.profile.publisher == obj.publisher)
                        or (obj in request.user.uploaded_books.all())\
                        or (obj in request.user.authored_books.all())):
                    return True
                else:
                    return False
            else: #editing permissions
                if obj.is_public() == True:
                    if request.user.is_staff:return True
                    
                else:
                    if request.user.is_staff\
                                            or ((request.user.profile.publisher == obj.publisher)
                                            or (obj in request.user.uploaded_books.all())\
                                            or (obj in request.user.authored_books.all())): return True                   
            
        return False

    
class BookViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.request.user.is_staff:
            return Book.objects.all()
        else:
            return Book.objects.filter(Q(isVerified=True,isPublished=True) | Q(uploader = self.request.user) | Q(author = self.request.user) | Q(publisher=self.request.user.profile.publisher))
   
   
    def get_serializer_class(self):
        '''if the user is admin, use the BookAdminSerializer. For any other user, the base serializer'''
        if self.request.user.is_staff:
            return BookAdminSerializer
        else: return BookSerializer
   
        

    queryset = Book.objects.get_queryset()
    
    filter_fields = ('isPublished','isVerified')
    permission_classes = (BookViewPermission,)


    def perform_create(self, serializer):
        data = self.request.data
        post_type = data.__getitem__('type')
        serializer.save(uploader=self.request.user)
        if post_type == 'write':
            serializer.save(author=self.request.user)
        else:
            serializer.save()

    def patch(self, request):
        data = request.data
        testmodel = (data.get('id'))
        serializer = BookSerializer(data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(code=202, data=serializer.data)
        return JsonResponse(code=400, data="wrong parameters")  

            

#display only the books with at least 2 users who favorite
class PopularBookViewSet(viewsets.ModelViewSet):

    #queryset = Book.objects.filter(users_who_favorite__gte=1).distinct()
    num_fans = 1
    queryset = Book.objects.annotate(users=Count('users_who_favorite')).filter(users__gte=num_fans) #filter out the books with num_fans users 
    serializer_class = BookSerializer

#identical to BookListView - but using generic views instead    
class BookList2(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

#a permission designed for UserViewSet -- only staff can see a list of all users. And only staff or the user itself can view a user detail page   
class IsStaffOrTargetUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow user to list all users if logged in user is staff
        return view.action == 'retrieve' or request.user.is_staff 
 
    def has_object_permission(self, request, view, obj):
        # allow logged in user to view own details, allows staff to view all records
        return request.user.is_staff or obj == request.user


class UserViewSet(viewsets.ModelViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (IsStaffOrTargetUser,)

class PublisherViewSet(viewsets.ModelViewSet): #publisher list - publishers can be created here
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
