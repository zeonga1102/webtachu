from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from books.models import BookModel
from users.models import ReviewModel


def genre_view(request, name):
    books = BookModel.objects.filter(genre=name)
    return render(request, 'main_genre/genre.html', {'books': books})

def detail_view(request, id):
    book_info = BookModel.objects.get(id=id)
    reviews = ReviewModel.objects.filter(book=book_info)

    return render(request, 'detail.html', {'book_info': book_info, 'reviews': reviews})


@login_required
def create_review_view(request, id):
    if request.method == 'POST':
        user = request.user
        book_info = BookModel.objects.get(id=id)
        star = request.POST.get('review', None)
        review = request.POST.get('review', None)

        ReviewModel.objects.create(user=user, book=book_info, star=star, desc=review)
        return redirect('book_info', id)


# @login_required
# def delete_review_view(request, id):
#
#
# @login_required