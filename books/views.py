from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from django.core.paginator import Paginator
from books.models import BookModel
from users.models import ReviewModel



def genre_view(request, name):
    books_list = BookModel.objects.filter(genre=name)
    page = request.GET.get('page', 1)
    paginator = Paginator(books_list, 10)
    pages = paginator.page(page)
    for book in books_list:
        book.star = book.star * 20

    book_all ={
        'pages' : pages,
        'name' : name,
        'books_list_num' : books_list.count(),
    }
    return render(request, 'main_genre/genre.html', {'book_all': book_all} )


def main_view(request):
    user = request.user
    likes = user.favorite.all()[::-1][:5]
    for book in likes:
        book.star = book.star * 20
    return render(request, 'main_genre/main.html', {'likes': likes})


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




