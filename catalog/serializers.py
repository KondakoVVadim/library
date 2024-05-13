from . import models
from rest_framework import serializers


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = '__all__'


class BookInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BookInstance
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'
