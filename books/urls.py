from books import views
from django.urls import path
from . import book_views



urlpatterns = [
    path('genre/<str:name>', views.genre_view, name='books'),
    path('home', views.genre_view, name='books'),
    path('<int:id>/', book_views.detail_view, name='book_info'),
]