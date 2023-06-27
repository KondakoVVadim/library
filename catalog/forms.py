from django import forms

from django.core.exceptions import ValidationError
import datetime
class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(label='Дата возврата',help_text="Введите дату между настоящим моментом и 4 неделями (по умолчанию 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(('Неверная дата - продление в прошлом'))

        elif data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(('Неверная дата - продление более чем на 4 недели вперед'))

        return data

from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'genre': forms.CheckboxSelectMultiple(),  # или forms.CheckboxSelectMultiple()
        }

