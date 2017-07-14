from __future__ import unicode_literals
from .api_views import BookViewPermission, BookViewSet, UserViewSet
from book_lovers.books.models import Profile, Book, Publisher
from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, mock
from .serializers import UserSerializer, BookSerializer
import unittest

from django.contrib.auth.hashers import is_password_usable, check_password
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from .api_views import BookViewPermission, BookViewSet, UserViewSet
from .factories import UserFactory, BookFactory
from .serializers import UserSerializer


@unittest.skipIf(False, "From before Author model removal")
class UserAPIViewTest(TestCase):

    # test the user view set creations, permissions, and functionality
    def setUp(self):
        self.detail_view = UserViewSet.as_view({'get': 'retrieve'})
        self.list_view = UserViewSet.as_view({'get': 'list', 'post': 'create'})

    def test_passwords(
            self):  # test that the password in the data input, and the password saved for the user are not equal
        data = {
            'username': 'aa',
            'email': 'b@gmail.com',
            'password': 'my_password',
            'fav_books': [],
        }

        newuser = UserSerializer().create(data)
        self.assertNotEqual(newuser.password,
                            data.get('password'))  # the password input is not saved as it's original string

        self.assertIsNotNone(newuser.password)  # user's password is not none
        self.assertTrue(is_password_usable(newuser.password))  # checks that a password appears hashed
        self.assertTrue(check_password(data.get('password'),
                                       newuser.password))  # confirms second param as proper hashing of first

    def test_detail_authenticate(self):

        # user's detail page should not be available unless user is authenticated
        request = APIRequestFactory().get("")
        bob_the_user = User.objects.create(username="bob")

        # user here is not authenticated - so even their own detail page they shouldn't be able to access
        response = self.detail_view(request, pk=bob_the_user.pk)
        self.assertNotEqual(response.status_code, 200)

        force_authenticate(request, user=bob_the_user)  # now, force user authentication
        response = self.detail_view(request, pk=bob_the_user.pk)
        self.assertEqual(response.status_code, 200)  # usr should be able to access their own detail page

    def test_detail_of_user(self):

        # test if a user can access their own detail page, but not another
        request = APIRequestFactory().get("")
        this_user = UserFactory()
        another_user = UserFactory()
        force_authenticate(request, user=this_user)

        response = self.detail_view(request, pk=another_user.pk)
        self.assertNotEqual(response.status_code,
                            200)  # this_user should not be able to access another_users's detail page

        response = self.detail_view(request, pk=this_user.pk)
        self.assertEqual(response.status_code, 200)  # this_user SHOULD be able to access the this_user detail page

    def test_admin(self):

        # test if an admin can access another user's detail page
        admin_user = UserFactory()
        admin_user.is_staff = True  # admin_user has admin permissions now
        non_admin_user = UserFactory()
        another_user = UserFactory()  # another non-admin user, for testing pk
        request = APIRequestFactory().get("")
        force_authenticate(request, user=non_admin_user)

        # non admin user
        response = self.detail_view(request, pk=another_user.pk)
        self.assertFalse(non_admin_user.is_staff)  # this user is not staff
        self.assertNotEqual(response.status_code, 200)  # this user shouldn't be able to access other user's detail page

        response = self.list_view(request)
        self.assertNotEqual(response.status_code, 200)  # non-admin user should not be able to access the list

        # admin user
        force_authenticate(request, user=admin_user)
        response = self.detail_view(request, pk=another_user.pk)
        self.assertTrue(admin_user.is_staff)  # this user is staff
        self.assertEqual(response.status_code, 200)  # this user is staff; should be able to access another's detail pg

        request = APIRequestFactory().get("")
        force_authenticate(request, user=admin_user)
        response = self.list_view(request)  # admin user should be able to access list view, and not a regular user
        self.assertEqual(response.status_code, 200)

    def test_create(self):

        # test if an admin user can create a new user and add it to the database with the post request
        admin_user = UserFactory()
        admin_user.is_staff = True  # is an admin
        user_data = {  # this data will be passed in for the post request
            'username': 'this_user',
            'email': 'user@example.com',
            'password': 'secretx',
            'fav_books': [],
            'uploaded_books': [],
            'authored_books': [],
        }
        request = APIRequestFactory().post("", user_data, format='json')
        force_authenticate(request, user=admin_user)
        response = self.list_view(request)
        self.assertEqual(response.status_code, 201)  # 201 status code -- means an object was created
        self.assertEqual(len(User.objects.all()), 2)  # there should now be 2 users - admin_user and this_user
        self.assertEqual(len(User.objects.filter
                             (username='this_user')), 1)  # there is now exactly one user, by the name of this_user


# testing for Author project
class AuthorProjectTests(TestCase):
    def setUp(self):
        self.view = BookViewSet.as_view({'get': 'list', 'get': 'retrieve', 'post': 'create', 'patch': 'partial_update'})
        self.detail_view = BookViewSet.as_view({'get': 'retrieve'})
        self.the_user = UserFactory()
        self.the_user.is_staff = False  # a regular user, not admin
        self.the_admin_user = UserFactory()
        self.the_admin_user.is_staff = True  # an admin user

    def to_dict(self, book):
        return {"title": book.title,
                "pen_name": book.pen_name,
                "publisher": book.publisher.pk,
                "users_who_favorite": [],
                "type": "upload"
                }

    def pub_to_dict(self, pub):
        return {"name": pub.name,
                "address": pub.address,
                "city": pub.city,
                "state_province": "",
                "country": ""}

    def test_upload_success(self):
        # when a post request is made to the book view with upload parameter, confirm that a book is created
        book = BookFactory.build()  # book is built but not saved (without a proper post, won't be found in database)
        book_data = self.to_dict(book)
        request = APIRequestFactory().post("", book_data, format="json")  # submit a post with this data, in JSON form
        force_authenticate(request, user=self.the_user)  # authenticated user
        response = self.view(request)
        self.assertEqual(response.status_code, 201)  # response should be 201- an object was created
        self.assertEqual(len(Book.objects.filter(title=book.title)),
                         1)  # there should be one book, with the title being book.title

    def test_write_success(self):
        # when a post request is made to the book view with write parameter, confirm that a book is created
        book = BookFactory.build()
        book_data = self.to_dict(book)
        book_data["type"] = "write"
        request = APIRequestFactory().post("", book_data,
                                           format="json")  # submit a post request with this data, in JSON form
        force_authenticate(request, user=self.the_user)  # authenticated user
        response = self.view(request)
        self.assertEqual(response.status_code, 201)  # response should be 201 status - an object was created
        self.assertEqual(len(Book.objects.filter(title=book.title)),
                         1)  # there should be one book, with the title being book.title

    def test_in_uploaded_books(self):
        # test that a book that's uploaded is added to user's uploaded_books and NOT to authored_books
        book = BookFactory.build()
        book_data = self.to_dict(book)
        request = APIRequestFactory().post("", book_data, format="json")
        force_authenticate(request, user=self.the_user)
        response = self.view(request)
        self.assertEqual(len(self.the_user.authored_books.filter(title=book.title)),
                         0)  # this was uploaded, so there should not be a book of this pk in authored_books
        self.assertEqual(len(self.the_user.uploaded_books.filter(title=book.title)),
                         1)  # should be 1 book, of this pk in the uploaded_books

    def test_in_uploaded_and_authored_books(self):
        # test that a book that's written is added to user's uploaded_books and to authored_books
        book = BookFactory.build()
        book_data = self.to_dict(book)
        book_data["type"] = 'write'
        request = APIRequestFactory().post("", book_data, format='json')
        force_authenticate(request, user=self.the_user)
        response = self.view(request)
        self.assertEqual(len(self.the_user.authored_books.filter(title=book.title)), 1)

        # this book was written by the user, so in authored_books, and uploaded by the user, so in uploaded_books
        self.assertEqual(len(self.the_user.uploaded_books.filter(title=book.title)), 1)

    def test_not_public_get_permissions(self):
        # If book isn't public, admin user or uploader should be able to access the detail page; but not a regular user
        book = BookFactory()
        book.isPublished = False
        book.isVerified = False  # book is not public
        self.assertIsNotNone(book.pk)  # book WAS created

        request = APIRequestFactory().get("")
        force_authenticate(request, user=self.the_user)  # request with a regular - non admin user
        response = self.detail_view(request, pk=book.pk)  # detail page of the not public book
        self.assertEqual(response.status_code, 404)  # the user should not be able to access this not public book

        request = APIRequestFactory().get("")
        force_authenticate(request, user=self.the_admin_user)  # request with an admin user
        response = self.view(request, pk=book.pk)  # detail page of the not public book
        self.assertEqual(response.status_code, 200)  # the admin user should be able to access this book detail page

        request = APIRequestFactory().get("")
        book.uploader = UserFactory()  # book_uploader is manually set as the book's uploader

        # book is added to uploaded_books of the user, as happens when a live request to server is made
        book.uploader.uploaded_books.add(book)
        force_authenticate(request, user=book.uploader)
        response = self.view(request, pk=book.pk)  # detail page of the not public book
        self.assertEqual(response.status_code, 200)  # book's uploader should be able to access this book detail page

    def test_is_verified_permissions(self):
        # is verified can be changed only by an admin - not by the book's uploader/author
        book = BookFactory()  # by default, isPublic() is false

        request = APIRequestFactory().patch("", {"isVerified": True})
        force_authenticate(request, user=self.the_admin_user)
        response = self.view(request, pk=book.pk)
        book.refresh_from_db()
        self.assertTrue(book.isVerified)  # admin user should be able to patch isVerified to True

        book = BookFactory()  # by default, isPublic() is false
        request = APIRequestFactory().patch("", {"isVerified": True})
        book.uploader = UserFactory()
        book.uploader.uploaded_books.add(book)

        force_authenticate(request, user=book.uploader)
        response = self.view(request, pk=book.pk)
        book.refresh_from_db()
        self.assertFalse(book.isVerified)  # the book's uploader should not be able to patch isVerified to True

    def test_is_published_permissions(self):
        # isPublished can be changed by the book's uploader/author, or by an admin user
        book = BookFactory()  # by default, isPublished is False
        request = APIRequestFactory().patch("", {"isPublished": True})
        force_authenticate(request, user=self.the_admin_user)
        response = self.view(request, pk=book.pk)
        book.refresh_from_db()
        self.assertTrue(book.isPublished)  # admin user should be able to patch isPublished to True

        book = BookFactory()
        request = APIRequestFactory().patch("", {"isPublished": True})
        book.uploader = UserFactory()
        book.uploader.uploaded_books.add(book)

        force_authenticate(request, user=book.uploader)
        response = self.view(request, pk=book.pk)
        book.refresh_from_db()
        self.assertTrue(book.isPublished)  # the book's uploader should be able to patch isPublished to True

    def test_object_modify_permissions(self):
        book = BookFactory()
        book.isPublished = True
        book.isVerified = True
        request1 = APIRequestFactory().patch("", {"title": "Test"})
        force_authenticate(request1, user=self.the_user)
        response = self.view(request1, pk=book.pk)
        self.assertFalse(BookViewPermission.has_object_permission(request1, request1, self.view, book))

        request2 = APIRequestFactory().patch("", {"title": "Test"})
        book.uploader = UserFactory()
        book.uploader.uploaded_books.add(book)
        force_authenticate(request2, user=book.uploader)
        response = self.view(request2, pk=book.pk)
        self.assertFalse(BookViewPermission.has_object_permission(request2, request2, self.view, book))

        request3 = APIRequestFactory().patch("", {"title": "Test"})
        force_authenticate(request3, user=self.the_admin_user)
        response = self.view(request3, pk=book.pk)
        self.assertTrue(BookViewPermission.has_object_permission(request3, request3, self.view, book))


class SerializerTests(TestCase):
    # test custom logic in the serializers
    def setUp(self):
        self.book_keys = ['id', 'title', 'pen_name', 'date', 'publisher',
                          'author', 'uploader', 'users_who_favorite', 'tags','text']  # all the keys expected to be serialized
        self.book_keys_write_only = ['isPublished', 'isVerified']

    def test_book_serializer_fields(self):
        test_book = BookFactory()
        serializer = BookSerializer(test_book)
        self.assertCountEqual(serializer.data.keys(), self.book_keys)  # check that serializer contains expected fields
        for each in self.book_keys_write_only:
            self.assertNotIn(each, serializer.data.keys())  # check that expected write only fields are not read
