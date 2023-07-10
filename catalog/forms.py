from django import forms

from django.core.exceptions import ValidationError
import datetime


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(label='Дата возврата',
                                   help_text="Введите дату между настоящим моментом и 4 неделями (по умолчанию 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(('Неверная дата - продление в прошлом жопа'))

        elif data > datetime.date.today() + datetime.timedelta(weeks=3):
            raise ValidationError(('Неверная дата - продление более чем на 4 недели вперед'))

        return data


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