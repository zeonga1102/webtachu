from books import views
from django.urls import path
from . import book_views



urlpatterns = [
    path('genre/<str:name>', views.genre_view, name='books'),
    path('home', views.genre_view, name='books'),
    path('<int:book_id>/', book_views.detail_view, name='book_info'),
    path('<int:book_id>/review/create/', views.create_review, name='create_review'),
    path('<int:book_id>/review/delete/<int:review_id>', views.delete_review, name='delete_review'),
    path('<int:book_id>/review/modify/<int:review_id>', views.modify_review, name='modify_review'),
]
