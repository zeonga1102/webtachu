from django.urls import path
from . import views

urlpatterns = [
    path('main', views.main_view, name='main'),
    path('genre/<str:name>', views.genre_view, name='genre'),
    path('genre/<str:name><int:page>', views.genre_view, name='paginator'),
]
