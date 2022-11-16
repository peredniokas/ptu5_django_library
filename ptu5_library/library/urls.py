from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.authors, name='authors'),
    path('author/<int:author_id>/', views.author, name='author'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book'),
    path('my_books/', views.UserBookListView.as_view(), name='user_books'),
]