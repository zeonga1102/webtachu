from books import views
from django.urls import path
from . import book_views


urlpatterns = [
    path('genre/<str:name>', views.genre_view, name='genre'),
    path('genre/<str:name><int:page>', views.genre_view, name='paginator'),
    path('main', views.main_view, name='main'),

    path('<int:id>/', book_views.detail_view, name='book_info'),
    path('favorite/<int:id>', book_views.book_favorite, name='book_favorite'),

    path('<int:book_id>/review/create/', views.create_review, name='create_review'),
    path('<int:book_id>/review/delete/<int:review_id>', views.delete_review, name='delete_review'),
    #path('<int:book_id>/review/modify/<int:review_id>', views.modify_review, name='modify_review'),
]
