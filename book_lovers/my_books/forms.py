
from django import forms
from .models import Book


class BookCreateForm(forms.ModelForm):
    class Meta:
        model = Book
     

class BookUpdateForm(BookCreateForm):
    def __init__(self, *args, **kwargs):
        super(BookUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Book
