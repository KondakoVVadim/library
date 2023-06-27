from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:id>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:id>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('my_books', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('all_borrowed', views.all_borrowed_books.as_view(), name='all-borrowed'),
    path('booki/<pk>/', views.renew_book_librarian, name='renew-book-librarian'),

]
# Редактирование, удаление и создание автора
urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<pk>/delete/', views.AuthorDelete.as_view(), name='author-delete')

]
# Редактирование, удаление и создание книги
urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<pk>/delete/', views.BookDelete.as_view(), name='book-delete')

]


urlpatterns += [
    path('return-book/<str:id>/', views.return_book, name='return-book'),
    path('bookInstance/create/', views.BookInstanceCreate.as_view(), name='bookInstance-create'),
    path('bookInstance/<pk>/update/', views.BookInstanceUpdate.as_view(), name='bookInstance-update'),
    path('bookInstance/<pk>/delete/', views.BookInstanceDelete.as_view(), name='bookInstance-delete'),

]

urlpatterns += [
    path('<str:id>', views.get_book)
]