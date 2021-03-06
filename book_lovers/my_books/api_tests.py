from __future__ import unicode_literals

from .api_views import BookViewPermission,BookViewSet,UserViewSet
from my_books.models import Profile,Book,Publisher,Author
from django.contrib.auth.models import User,AnonymousUser
from django.test import TestCase,mock
from .serializers import UserSerializer
from django.contrib.auth.hashers import is_password_usable,check_password
from rest_framework.test import APIRequestFactory,force_authenticate,APIClient
from .factories import UserFactory
#from rest_framework.reverse import reverse


class BookViewPermissionTest(TestCase, BookViewPermission):

    def setUp(self):
        author = Author.objects.create(name='Author')
        publisher = Publisher.objects.create(name='Apress')
        pub = Publisher.objects.create(name='Irrelevant')

        pu = Book.objects.create(title="Published", publisher=pub ,isPublished=True)
        up = Book.objects.create(title="Unpublished", publisher=publisher, isPublished=False)
        pu.save()
        up.save()
        pu.author.add(author)
        up.author.add(author)

    @mock.patch('requests.get')
    def test_permissions(self,mockget):
        pu = Book.objects.get(title="Published")
        up = Book.objects.get(title="Unpublished")
        pu.save()
        up.save()

        user1 = User(id=1, username="a", password="A", email='A@a.com')
        user2 = User(id=2, username="b", password="B", email='B@b.com')
        user3 = User(id=3, username="c", password="C", email='C@c.com')
        user4 = AnonymousUser()
        user1.save()
        user2.save()
        user3.save()

        profile1 = Profile.objects.create(user=user1, publisher=pu.publisher)
        profile2 = Profile.objects.create(user=user2, publisher=up.publisher)
        profile3 = Profile.objects.create(user=user3, publisher=pu.publisher)

        user1.owned_books.add(pu)
        user3.owned_books.add(up)

        myView = BookViewSet
        myView.request = mockget.requests.get

        # TEST 1: test if the user can access the Book list page
        # TEST 2: test if the user can access Book 1
        # TEST 3: test if the user can access Book 2

        myView.request.user = user1

        # yes - user is authenticated
        self.assertTrue(BookViewPermission.has_permission(myView.request, myView.request, myView))

        # yes - book is published
        self.assertTrue(BookViewPermission.has_object_permission(myView.request,myView.request,myView,pu))

        # no - book is unpublished, and user doesn't work for publisher or own the book
        self.assertFalse(BookViewPermission.has_object_permission(myView.request,myView.request,myView,up))

        myView.request.user = user2

        # yes - user is authenticated
        self.assertTrue(BookViewPermission.has_permission(myView.request, myView.request, myView))

        # yes - book is published
        self.assertTrue(BookViewPermission.has_object_permission(myView.request, myView.request, myView, pu))

        # yes - user works for the publisher
        self.assertTrue(BookViewPermission.has_object_permission(myView.request, myView.request, myView, up))

        myView.request.user = user3

        # yes - user is authenticated
        self.assertTrue(BookViewPermission.has_permission(myView.request, myView.request, myView))

        # yes - book is published
        self.assertTrue(BookViewPermission.has_object_permission(myView.request, myView.request, myView, pu))

        # yes - user owns the book
        self.assertTrue(BookViewPermission.has_object_permission(myView.request, myView.request, myView, up))

        myView.request.user = user4

        # NO to all - user is not authenticated
        self.assertFalse(BookViewPermission.has_permission(myView.request, myView.request, myView))
        self.assertFalse(BookViewPermission.has_object_permission(myView.request, myView.request, myView, pu))
        self.assertFalse(BookViewPermission.has_object_permission(myView.request, myView.request, myView, up))
        

class UserAPIViewTest(TestCase):
    '''test the user view set creations, permissions, and functionality'''
    def setUp(self):
        self.detail_view = UserViewSet.as_view({'get':'retrieve'})
        self.list_view = UserViewSet.as_view({'get':'list','post':'create'})
   
    def test_passwords(self): #test that the password in the data input, and the password saved for the user are not equal
        data = {
            'username':'aa',
            'email':'b@gmail.com',
            'password':'my_password',
            'fav_books': [],
            'owned_books':[]
            }
        newUser = UserSerializer().create(data)
        self.assertNotEqual(newUser.password, data.get('password')) #the password input is not saved as it's original string
        self.assertIsNotNone(newUser.password) #user's password is not none
        self.assertTrue(is_password_usable(newUser.password)) #checks that a password appears hashed
        self.assertTrue(check_password(data.get('password'),newUser.password)) #confirms that the second param is a proper hashing of the first
        
    def test_detail_authenticate(self):
        '''user's detail page should not be available unless user is authenticated '''
        request = APIRequestFactory().get("")
        bob_the_user = User.objects.create(username="bob") 
        response = self.detail_view(request, pk=bob_the_user.pk) #user here is not authenticated - so even their own detail page they shouldn't be able to access
        self.assertNotEqual(response.status_code, 200)
         
        force_authenticate(request,user = bob_the_user) #now, force user authentication
        response = self.detail_view(request, pk=bob_the_user.pk)
        self.assertEqual(response.status_code, 200)   #usr should be able to access their own detail page 
   
    def test_detail_of_user(self):
        '''test if a user can access their own detail page, but not another'''
        request = APIRequestFactory().get("")
        this_user = UserFactory()
        another_user = UserFactory()
        force_authenticate(request,user = this_user)
       
        response = self.detail_view(request,pk = another_user.pk)
        self.assertNotEqual(response.status_code,200) #this_user should not be able to access another_users's detail page
        
        response = self.detail_view(request,pk = this_user.pk)
        self.assertEqual(response.status_code, 200) #this_user SHOULD be able to access the this_user detail page
        
    def test_admin(self):
        '''test if an admin can access another user's detail page'''
        admin_user = UserFactory()
        admin_user.is_staff = True #admin_user has admin permissions now
        non_admin_user = UserFactory()
        another_user = UserFactory() #another non-admin user, for testing pk
        request = APIRequestFactory().get("")
        force_authenticate(request,user = non_admin_user)
    
        #non admin user
        response = self.detail_view(request,pk = another_user.pk) 
        self.assertFalse(non_admin_user.is_staff) #this user is not staff
        self.assertNotEqual(response.status_code,200) #this user should not be able to access another user's detail page
        
        response = self.list_view(request)
        self.assertNotEqual(response.status_code,200) #non-admin user should not be able to access the list 
    
        #admin user
        force_authenticate(request,user = admin_user)
        response = self.detail_view(request,pk = another_user.pk)
        self.assertTrue(admin_user.is_staff) #this user is staff
        self.assertEqual(response.status_code,200) #since this user is staff, should be able to access another's detail page
        
        response = self.list_view(request) #admin user should be able to access list view, and not a regular user
        self.assertEqual(response.status_code,200)
        
    def test_create(self):
        '''test if an admin user can create a new user and add it to the database with the post request'''
        admin_user = UserFactory()
        admin_user.is_staff = True #is an admin 
        user_data = {        #this data will be passed in for the post request
            'username':'this_user',
            'email':'user@example.com',
            'password':'secretx',
            'fav_books':[],
            'owned_books':[]
            }
        request = APIRequestFactory().post("",user_data,format = 'json')
        force_authenticate(request, user = admin_user)
        response = self.list_view(request)
        self.assertEqual(response.status_code, 201) #201 status code -- means an object was created
        self.assertEqual(len(User.objects.all()),2) #there should now be 2 users - admin_user and this_user
        self.assertEqual(len(User.objects.filter(username = 'this_user')),1) #there is now exactly one user, by the name of this_user