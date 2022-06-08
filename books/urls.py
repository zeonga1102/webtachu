from books import views
from django.urls import path
from . import book_views



urlpatterns = [
    path('genre/<str:name>', views.genre_view, name='genre'),
    path('genre/<str:name>/<int:page>', views.genre_view, name='genre_paginator'),
    path('<int:id>/', book_views.detail_view, name='book_info'),
    path('main', views.main_view, name='main'),
]
