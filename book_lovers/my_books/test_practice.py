from .factories import UserFactory,BookFactory,PublisherFactory
from .serializers import BookSerializer, PublisherSerializer
from django.test import TestCase

class CreationTests(TestCase):
    
    def test_make_user(self):
        user = UserFactory()
        self.assertEqual(user, user.profile.user)
    
    def to_dict(self,book):
        return {"title":book.title,
                "pen_name":book.pen_name,
                "publisher":book.publisher,
                "uploader":book.uploader,
                "author":book.author,
                "users_who_favorite": None,
                "type":"upload"
                }        
    
    def test_make_book(self):
        book = BookFactory()
        #print(book.author.username)
        #print(book.uploader.username)
        #print(BookSerializer(book))
        book = BookFactory()
        book_dict  = self.to_dict(book)
        serializer = BookSerializer(book)
        print(serializer.data)
        print("Now as dictionary passed in")
        serializer = BookSerializer(data = book_dict)
        print(serializer.initial_data)
     
        
        
    def test_publisher_serializer(self):
        pub = PublisherFactory()
        #print(PublisherSerializer(pub))
        Book = BookFactory()
        pub = Book.publisher
        #print(PublisherSerializer(pub))
    