from __future__ import unicode_literals

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from book_lovers.books.factories import BookFactory
from book_lovers.books.models import Book
from book_lovers.users.factories import UserFactory
from .serializers import BookSerializer
from .views import BookViewPermission, BookViewSet


# testing for author update - previous model, author, was removed from the database and replaced with pen_name, and 2
# one-many relationships with User: uploader and author
class AuthorUploaderTests(TestCase):
    def setUp(self):
        self.view = BookViewSet.as_view(actions={'get': 'list', 'get': 'retrieve', 'post': 'create',
                                                 'patch': 'partial_update'})
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
        response = self.view(request, pk=book.pk)  # detail page of the not public book
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
    # test custom logic in the book serializers
    def setUp(self):
        self.book_keys = ['id', 'title', 'pen_name', 'date', 'publisher',
                          'author', 'uploader', 'users_who_favorite', 'tags',
                          'text']  # all the keys expected to be serialized
        self.book_keys_write_only = ['isPublished', 'isVerified']

    def test_book_serializer_fields(self):
        test_book = BookFactory()
        serializer = BookSerializer(test_book)
        self.assertCountEqual(serializer.data.keys(), self.book_keys)  # check that serializer contains expected fields
        for each in self.book_keys_write_only:
            self.assertNotIn(each, serializer.data.keys())