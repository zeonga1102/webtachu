from django.urls import path
from . import book_views


urlpatterns = [
    path('<int:id>/', book_views.detail_view, name='book_info'),
]
