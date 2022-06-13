from django.shortcuts import render
from django.core.paginator import Paginator
from books.models import BookModel
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

    book_all = {
        'pages': pages,
        'name': name,
        'books_list_num': books_list.count(),
    }
    return render(request, 'main_genre/genre.html', {'book_all': book_all})


def main_view(request):
    user = request.user

    cursor = connection.cursor()
    query = "SELECT * FROM users_favorite WHERE usermodel_id=%s" % user.id
    cursor.execute(query)
    stocks = cursor.fetchall()

    stocks_length = len(stocks)
    if stocks_length > 5:
        stocks_length = 5

    stocks.sort(key=lambda x: -x[0])

    favorite = []
    for i in range(stocks_length):
        fav = user.favorite.get(id=stocks[i][2])
        fav.star = fav.star * 20
        favorite.append(fav)

    li_list = get_today_20()

    favorite_all = user.favorite.all()

    datas = []
    if len(favorite_all) == 0:
        books = BookModel.objects.all().order_by('-star')[:5]
        for book in books:
            datas.append(book)

    else:
        title_keyword = make_keyword(favorite_all, 'title', 3) * 3
        keyword = make_keyword(favorite_all, 'story', 20)
        keyword += title_keyword
        keyword_vec = model.infer_vector(keyword)
        most_similar = model.docvecs.most_similar([keyword_vec], topn=favorite_all.count() + 5)
        for index, similarity in most_similar:
            recommend = BookModel.objects.get(id=index + 1)
            if not recommend in favorite_all:
                datas.append(recommend)
            if len(datas) == 5:
                break

    for book in datas:
        book.star = book.star * 20

    return render(request, 'main_genre/main.html', {'likes': favorite, 'li_list': li_list, 'datas': datas})


def search(request, title):
    result = BookModel.objects.filter(title__icontains=title)
    page = request.GET.get('page', 1)
    paginator = Paginator(result, 10)
    pages = paginator.page(page)

    for page in pages:
        page.star = page.star * 20

    result_info = {
        'pages': pages,
        'name': f"'{title}'의 검색 결과",
        'books_list_num': result.count(),
    }
    return render(request, 'main_genre/genre.html', {'book_all': result_info})


def get_today_20():
    url = 'https://series.naver.com/novel/top100List.series?rankingTypeCode=DAILY&categoryCode=ALL'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
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

        star_width = float(star) * 10 - 2.3

        dic = {'url': url, 'cover': cover_m260, 'title': title, 'author': author, 'author': author, 'star': star,
               'star_width': star_width, 'detail': detail}

        li_list.append(dic)

    return li_list
