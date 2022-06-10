from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from books.models import BookModel
from users.models import ReviewModel
from django.utils import timezone
from django.db import connection
import requests
from bs4 import BeautifulSoup
from gensim.models.doc2vec import Doc2Vec
from .book_views import make_keyword


model = Doc2Vec.load('model.doc2vec')


def genre_view(request, name):
    books_list = BookModel.objects.filter(genre=name)
    page = request.GET.get('page', 1)
    paginator = Paginator(books_list, 10)
    pages = paginator.page(page)

    for page in pages:
        page.star = page.star * 20

    book_all ={
        'pages' : pages,
        'name' : name,
        'books_list_num' : books_list.count(),
    }
    return render(request, 'main_genre/genre.html', {'book_all': book_all} )


def main_view(request):
    user = request.user

    cursor = connection.cursor()
    query = "SELECT * FROM users_favorite WHERE usermodel_id=%s" % (user.id)
    cursor.execute(query)
    stocks = cursor.fetchall()
    stocks.sort(key=lambda x: -x[0])

    stocks_length = len(stocks)
    if stocks_length > 5:
        stocks_length = 5

    favorite = []
    for i in range(stocks_length):
        fav = user.favorite.get(id=stocks[i][2])
        fav.star = fav.star * 20
        favorite.append(fav)

    li_list = get_today_20()

    favorite_all = user.favorite.all()
    keyword = make_keyword(favorite_all, 'story', 20)
    keyword_vec = model.infer_vector(keyword)
    most_similar = model.docvecs.most_similar([keyword_vec], topn=5)

    datas = []
    for index, similarity in most_similar:
        datas.append(BookModel.objects.get(id=index+1))

    for book in datas:
        book.star = book.star * 20

    return render(request, 'main_genre/main.html', {'likes': favorite, 'li_list':li_list, 'datas': datas})


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

    if review_count == 1:
        new_avg = 0
    else:
        new_avg = (current_book.star * review_count - star) / (review_count - 1)
    current_book.star = new_avg
    current_book.save()

    return redirect('book_info', book_id)


@login_required
def modify_review(request, book_id, review_id):
    origin_review = ReviewModel.objects.filter(id=review_id)

    if request.method == "POST":
        star = int(request.POST.get('rating', 0))
        review = request.POST.get('review', '')
        date = timezone.now()

        origin_review.update(star=star, desc=review, date=date)

        return redirect('book_info', book_id)


def get_today_20():
    url = 'https://series.naver.com/novel/top100List.series?rankingTypeCode=DAILY&categoryCode=ALL'

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url,headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    lis = soup.select('#content > div > ul > li')

    li_list = []

    for li in lis:
        url = 'https://series.naver.com' + li.select_one('a')['href']
        cover_line = li.select_one('a > img')
        cover_m79 = cover_line['src']
        cover_m260 = cover_m79.replace("type=m79", "type=m260")
        title = cover_line['alt']
        author = li.select_one('div.comic_cont > p.info > span:nth-child(4)').text
        star = li.select_one('div.comic_cont > p.info > em.score_num').text
        detail = li.select_one('div.comic_cont > p.info > span:nth-child(6)').text

        star_width = float(star) * 10

        dic = {'url':url, 'cover':cover_m260, 'title':title, 'author':author, 'author':author, 'star':star, 'star_width':star_width, 'detail':detail}

        li_list.append(dic)

    return li_list
