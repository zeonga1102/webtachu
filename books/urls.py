from django.urls import path
from . import book_views, review_views, views


urlpatterns = [
    path('main', views.main_view, name='main'),
    path('genre/<str:name>', views.genre_view, name='genre'),
    path('genre/<str:name><int:page>', views.genre_view, name='paginator'),

    path('<int:id>/', book_views.detail_view, name='book_info'),
    path('favorite/<int:id>', book_views.book_favorite, name='book_favorite'),

    path('<int:book_id>/review/create/', review_views.create_review, name='create_review'),
    path('<int:book_id>/review/delete/<int:review_id>', review_views.delete_review, name='delete_review'),
    path('<int:book_id>/review/modify/<int:review_id>', review_views.modify_review, name='modify_review'),
    
    path('search/<str:title>', views.search, name='search'),
]
