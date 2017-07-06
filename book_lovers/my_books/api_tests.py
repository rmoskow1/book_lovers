from django.test import TestCase
from .serializers import UserSerializer
from django.contrib.auth.hashers import is_password_usable,check_password
from rest_framework.test import APIRequestFactory,force_authenticate,APIClient
from .api_views import UserViewSet
from django.contrib.auth.models import User
from .factories import UserFactory
#from rest_framework.reverse import reverse

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