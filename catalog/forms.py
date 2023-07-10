from django import forms

from django.core.exceptions import ValidationError
import datetime


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(label='Дата возврата',
                                   help_text="Введите дату между настоящим моментом и 4 неделями (по умолчанию 3).")


from .models import Book, Author, BookInstance


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'genre': forms.CheckboxSelectMultiple(),  # или forms.CheckboxSelectMultiple()
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_death': forms.DateInput(attrs={'type': 'date'})
        }
        initial = {
            'date_of_birth': '2000-01-01',
            'date_of_death': '2016-10-12'
        }

class BookInstanceForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = '__all__'