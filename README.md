# book_lovers

This project is a simple program for a book database, with functionality to edit this database online. The main purpose of this project is to serve as an introduction to Django and Django Rest Framework for developers. 

Project features:
- models: Books, Authors, Publishers, Tags, and Users. 
- functionality: Model instances can be created, deleted and updated. Books can be searched for by book title, author name, publisher name, or tag. 
- permissions: Anonymous users can view database. Authenticated users can add/delete instances, can update existing books, and can add books to their favorites list. 
Note: this project is centered around the Book model - this is the only model to have all other models as foreign keys, amd searching functionality is for books. .

API documentation can be found in the "docs" page. 
