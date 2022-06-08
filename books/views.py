from django.shortcuts import render
from books.models import BookModel


def genre_view(request, name):
    books = BookModel.objects.filter(genre=name)
    return render(request, 'genre.html', {'books': books})