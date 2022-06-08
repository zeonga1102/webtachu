from books import views
from django.urls import path



urlpatterns = [
    path('genre/<str:name>', views.genre_view, name='books'),
    path('home', views.genre_view, name='books'),
]