from django.shortcuts import render
from books.models import BookModel


# def genre_view(request, name):
#     books = BookModel.objects.filter(genre=name)
#     return render(request, 'genre.html', {'books': books})

def genre_view(request, name):
    books = BookModel.objects.filter(genre=name)
    return render(request, 'genre.html', {'books': books})

# 메인페이지
# def home_view(request, name):
#     books = BookModel.objects.filter(genre=name)
#     return render(request, 'genre.html', {'books': books})