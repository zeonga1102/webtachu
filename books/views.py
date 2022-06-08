from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from books.models import BookModel
from users.models import ReviewModel
from django.db.models import Count, Avg


def genre_view(request, name):
    books = BookModel.objects.filter(genre=name)
    return render(request, 'main_genre/genre.html', {'books': books})


@login_required
def create_review(request, book_id):
    if request.method == 'POST':
        user = request.user
        current_book = BookModel.objects.get(id=book_id)
        star = int(request.POST.get('rating', 0))
        review = request.POST.get('review', '')

        ReviewModel.objects.create(user=user, book=current_book, star=star, desc=review)
        return redirect('book_info', book_id)


@login_required
def delete_review(request, book_id, review_id):
    review = ReviewModel.objects.get(id=review_id)
    review.delete()
    return redirect('book_info', book_id)


# @login_required
# def modify_review(request, book_id, review_id):
#     if request.method == "POST":
#         review = ReviewModel.objects.get(id=review_id)
