from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from books.models import BookModel
from users.models import ReviewModel
from django.utils import timezone
import requests
from bs4 import BeautifulSoup



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
    li_list = get_today_20()
    for book in likes:
        book.star = book.star * 20
    return render(request, 'main_genre/main.html', {'likes': likes, 'li_list':li_list})


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
        current_book.star = new_avg
        current_book.save()

        return redirect('book_info', book_id)


@login_required
def delete_review(request, book_id, review_id):
    review = ReviewModel.objects.get(id=review_id)
    current_book = BookModel.objects.get(id=book_id)
    review_count = ReviewModel.objects.filter(book=current_book).count()

    star = review.star

    review.delete()

    new_avg = (current_book.star * review_count - star) / (review_count - 1)
    current_book.star = new_avg
    current_book.save()

    return redirect('book_info', book_id)


# @login_required
# def modify_review(request, book_id, review_id):
#     origin_review = ReviewModel.objects.get(id=review_id)
#
#     if request.method == "POST":
#         star = int(request.POST.get('rating', 0))
#         review = request.POST.get('review', '')
#         date = timezone.now()
#
#         origin_review.objects.update(star=star, desc=review, date=date)
#         modify_review = True
#         return redirect('book_info', book_id, modify_review)


def get_today_20():
    url = 'https://series.naver.com/novel/top100List.series?rankingTypeCode=DAILY&categoryCode=ALL'

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url,headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    lis = soup.select('#content > div > ul > li')

    li_list = []

    for li in lis:
        cover_line = li.select_one('a > img')
        cover_m79 = cover_line['src']
        cover_m260 = cover_m79.replace("type=m79", "type=m260")
        title = cover_line['alt']
        author = li.select_one('div.comic_cont > p.info > span:nth-child(4)').text
        star = li.select_one('div.comic_cont > p.info > em.score_num').text
        detail = li.select_one('div.comic_cont > p.info > span:nth-child(6)').text

        star_width = float(star) * 10

        dic = {'cover':cover_m260, 'title':title, 'author':author, 'author':author, 'star':star, 'star_width':star_width, 'detail':detail}

        li_list.append(dic)

    return li_list
