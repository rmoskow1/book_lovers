
from django.views.generic import ListView
from django.test import TestCase, RequestFactory
from .models import Book
from .views import BookSearchMixin, FavoritesListView
from .factories import BookFactory
from my_books.factories import UserFactory


# book search needs to test: 1.empty queryset 2.returning all values with the search in the author name
# 3.values with the search in the title 4.values with the exact search being the tag name
# 5. when a book is an answer for more than one category, it shouldn't appear twice


class BookSearchMixinTest(TestCase):
    """based on @dnmellen - tests mixin within a fake template"""

    class DummyView(BookSearchMixin, ListView):
        model = Book

        template_name = "best_darn_template_eva.html"  # needed to be defined for any TemplateView

    def setUp(self):
        super(BookSearchMixinTest, self).setUp()
        self.View = self.DummyView()

    def assert_list_query(self, list, querySet):  # simple helper method for checking a list and queryset are equal
        for i in list:
            self.assertIn(i, querySet)  # every book in the list is in the queryset
        self.assertEqual(len(list), len(querySet))  # the 2 contain the same number of elements

    def test_pub_search(self):
        """test if search successfully finds all books with publisher names containing the search query"""
        # make some books with specific publisher names
        book1 = BookFactory.create(title="book1", publisher__name="aaa")
        book2 = BookFactory.create(title="book2", publisher__name="bbb")
        book3 = BookFactory.create(title="book3", publisher__name="ccc")
        book4 = BookFactory.create(title="book4", publisher__name="abdc")
        # 'a' search - not in the book title
        request = RequestFactory().get("/fake", {"q": "a"})
        self.View.request = request
        expected_books = [book1, book4]
        actual_books = self.View.get_queryset()
        self.assert_ListQuery(expected_books, actual_books)


    def test_author_search(self):
        """test if the search successfully finds all books with author names containing the search query"""
        # make some books, titles can be random but author names are specific
        book1 = BookFactory.create(title="book1", publisher__name="pub", pen_name="bbb"),
        book2 = BookFactory.create(title="book2", publisher__name="pub", pen_name="aaa"),
        book3 = BookFactory.create(title="book3", publisher__name="pub", pen_name="ccc"),
        book5 = BookFactory.create(title="book5", publisher__name="pub", pen_name="lll"),
        book4 = BookFactory.create(title="book4", publisher__name="pub", pen_name="abc"),
        # 'a' search - not in the book title
        request = RequestFactory().get("/fake", {"q": "a"})
        self.View.request = request
        expected_books = [book1, book2, book4]
        actual_books = self.View.get_queryset()
        self.assert_ListQuery(expected_books, actual_books)

    def test_title_search(self):
        # test - the resulting queryset should just be the view's queryset properly filtered
        book1 = BookFactory.create(title="Best Book")
        book2 = BookFactory.create(title="Worst Book")
        request = RequestFactory().get("/fake/path", {'q': "Best"})
        self.View.request = request
        expected_books = [book1]
        actual_books = self.View.get_queryset()
        self.assert_ListQuery(expected_books, actual_books)

    def test_case_ins(self):
        """test for case insensitivity when searching"""
        book1 = BookFactory.create(title="Best book")
        book2 = BookFactory.create(title="best")
        book3 = BookFactory.create(title="bESt")
        # now testing variety among entry capitalization
        request = RequestFactory().get("/fake/path", {'q': "Best"})
        self.View.request = request
        expected_books = [book1, book2, book3]
        actual_books = self.View.get_queryset()
        self.assert_ListQuery(expected_books, actual_books)
        #even with different cases in the title, all the books will be found

        #now testing that a query with different cases will return the same queryset
        request2 = RequestFactory().get("/fake/path", {'q': "BEST"})
        self.View.request = request2
        expected_books = [book1, book2, book3]
        actual_books = self.View.get_queryset()
        self.assert_ListQuery(expected_books, actual_books)

    def test_multiples(self):
        bookList = BookFactory.create_batch(
            size=15)  # create a random collection of books with fuzzy titles, author names, publisher names, etc.
        request = RequestFactory().get("fake/path", {'q': 'e'})
        self.View.request = request
        actual_books = self.View.get_queryset()
        countList = []
        for book in actual_books:
            if book not in countList:
                countList.append(book)
            else:  # if book IS in countList
                self.assertFalse(True)  # the query was not distinct!


# BookDeleteView uses only built-in DeleteView functionality - doesn't need to be tested here
# BookListView uses only built-in ListView functionality - doesn't need to be tested here


class FavoritesListViewTest2(TestCase):  # 1 is Pinchas's, 2 is Racheli's
    """tests that the FavoritesListView correctly displays a list of the user's favorite books """

    def setup(self):
        super(FavoritesListViewTest2, self).setUp()

    def test_listing(self):
        request = RequestFactory().get("fake/path")
        # book1 = BookFactory()
        # book2 = BookFactory()
        request.user = UserFactory()  # create a user with user factory, and assign this to the request made
        bob = request.user  # request from sruli...he thinks every user deserves a loving name
        expected_books = bob.fav_books.all()
        view = FavoritesListView()
        view.request = request
        actual_books = view.get_queryset()
        for book in expected_books:
            self.assertIn(book, actual_books)
        self.assertEqual(len(actual_books), len(expected_books))

