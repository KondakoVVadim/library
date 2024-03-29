from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

from django.urls import reverse  # To generate URLS by reversing URL patterns


class Genre(models.Model):
    name = models.CharField(max_length=20, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    date_of_death = models.DateField(null=True, blank=True, verbose_name='Дата смерти')

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)


class Language(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        return self.name


from django.urls import reverse
import uuid  # Required for claunique book instances


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Уникальный идентификатор этой конкретной книги во всей библиотеке")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, verbose_name='Книга')
    imprint = models.CharField(max_length=200, verbose_name='Номер')
    due_back = models.DateField(null=True, blank=True, verbose_name='Дата возврата')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Заемщик')
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Доступно'),
        ('r', 'Reserved'),
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability',
                              verbose_name='Статус')

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s)' % (self.id, self.book.title)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Book(models.Model):
    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'
    title = models.CharField(max_length=40, verbose_name='Название')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book",
                               verbose_name='Описание')
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book", verbose_name='Жанр')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, verbose_name='Язык')

    class Meta:
        ordering = ['title', 'author']

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        return self.title
