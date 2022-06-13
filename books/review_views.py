from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from books.models import BookModel
from users.models import ReviewModel
from django.utils import timezone


@login_required
def create_review(request, book_id):
    if request.method == 'POST':
        user = request.user
        current_book = BookModel.objects.get(id=book_id)
        review_count = ReviewModel.objects.filter(book=current_book).count()

        star = int(request.POST.get('rating', 0))
        review = request.POST.get('review', '')

        ReviewModel.objects.create(user=user, book=current_book, star=star, desc=review)

        new_avg = (current_book.star * review_count + star) / (review_count + 1)
        current_book.star = round(new_avg, 1)
        current_book.save()

        return redirect('book_info', book_id)


@login_required
def delete_review(request, book_id, review_id):
    review = ReviewModel.objects.get(id=review_id)
    current_book = BookModel.objects.get(id=book_id)
    review_count = ReviewModel.objects.filter(book=current_book).count()

    star = review.star

    review.delete()

    if review_count == 1:
        new_avg = 0
    else:
        new_avg = (current_book.star * review_count - star) / (review_count - 1)
        new_avg = round(new_avg, 1)
    current_book.star = new_avg
    current_book.save()

    return redirect('book_info', book_id)


@login_required
def modify_review(request, book_id, review_id):
    origin_review = ReviewModel.objects.filter(id=review_id)
    print(origin_review[0].star)

    if request.method == "POST":
        star = int(request.POST.get('rating', 0))
        review = request.POST.get('review', '')
        date = timezone.now()

        current_book = BookModel.objects.get(id=book_id)
        review_count = ReviewModel.objects.filter(book=current_book).count()
        new_avg = (current_book.star * review_count - origin_review[0].star + star) / review_count
        current_book.star = round(new_avg, 1)
        current_book.save()

        origin_review.update(star=star, desc=review, date=date)

        return redirect('book_info', book_id)
