from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/', views.BookListView.as_view(), name='books'),
    path('book/<int:id>', views.BookDetailView.as_view(), name='book-detail'),
]
