from django.shortcuts import render
from books.models import BookModel
from django.core.paginator import Paginator


# def genre_view(request, name):
#     books = BookModel.objects.filter(genre=name)
#     return render(request, 'main_genre/genre.html', {'books': books})

def genre_view(request, name):
    books_list = BookModel.objects.filter(genre=name)
    page = request.GET.get('page', '1')
    paginator = Paginator(books_list, 10)
    pages = paginator.page(page)
    return render(request, 'main_genre/genre.html', {'pages': pages})


def main_view(request):
    return render(request, 'main_genre/main.html')