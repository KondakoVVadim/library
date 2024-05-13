from rest_framework.generics import ListAPIView
from . import serializers
from . import models


class GenreListAPIView(ListAPIView):
    serializer_class = serializers.GenreSerializer

    def get_queryset(self):
        return models.Genre.objects.all()


class AuthorListAPIView(ListAPIView):
    serializer_class = serializers.AuthorSerializer

    def get_queryset(self):
        return models.Author.objects.all()

class BookInstanceListAPIView(ListAPIView):
    serializer_class = serializers.BookInstanceSerializer

    def get_queryset(self):
        return models.BookInstance.objects.all()

class BookListAPIView(ListAPIView):
    serializer_class = serializers.BookSerializer

    def get_queryset(self):
        return models.Book.objects.all()
