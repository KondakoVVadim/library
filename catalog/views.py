from django.shortcuts import render
# Create your views here.

from .models import Book, Author, BookInstance, User, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RenewBookForm

from django import forms
from django.core.exceptions import ValidationError

from .forms import BookForm, AuthorForm

import datetime


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """

    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # Метод 'all()' применён по умолчанию.

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    # if request.method == 'GET':
    #     return render(
    #     request,
    #     'catalog/index.html',
    #     context={'num_books': num_books, 'num_instances': num_instances,
    #              'num_instances_available': num_instances_available, 'num_authors': num_authors},
    # )
    return render(
        request,
        'catalog/index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors},
    )


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('q', '')
        query_list = self.request.GET.getlist('chekbox', '')
        if query:
            results = Book.objects.filter(title__icontains=query).order_by('title')
            context = {'results': results, 'query': query}
            return context
        elif query_list:
            if len(query_list) == 1:
                results = Book.objects.filter(genre__in=query_list[0]).distinct()
                context = {'results': results, 'query2': query_list}
                return context
            if len(query_list) > 1:
                results = Book.objects.filter(genre__in=query_list).distinct()
                context = {'results': results, 'query2': query_list}
                return context
        # В первую очередь получаем базовую реализацию контекста
        context = super(BookListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        context['genre'] = Genre.objects.all()
        return context




class BookDetailView(generic.TemplateView):
    template_name = 'catalog/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = kwargs['id']
        book = Book.objects.get(id=id)
        context['book'] = book
        return context


class AuthorListView(generic.ListView):
    model = Author

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('q', '')
        if query:
            results = Author.objects.filter(first_name__icontains=query)
            context = {'results': results, 'query': query}
            return context
        # В первую очередь получаем базовую реализацию контекста
        context = super(AuthorListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        context['search'] = 'This is just some data'
        return context


class AuthorDetailView(generic.TemplateView):
    template_name = 'catalog/author_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = kwargs['id']
        author = Author.objects.get(id=id)
        context['author'] = author
        return context


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Вместо LoginRequiredMixin можно просто использовать декоратор @login_required
    импортировав из django.contrib.auth.decorators
    """

    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        today = datetime.date.today()

        if data < today:
            raise ValidationError('Неверная дата - продление в прошлом')
        # elif data > today + datetime.timedelta(weeks=4):
        #     raise ValidationError('Неверная дата - продление более чем на 4 недели вперед')

        return data


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']

            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date, })

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})


@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy('login')), name='dispatch')
class all_borrowed_books(generic.ListView):
    """
    Вместо LoginRequiredMixin можно просто использовать декоратор @login_required
    импортировав из django.contrib.auth.decorators
    """

    model = BookInstance
    template_name = 'catalog/all_borrowed_books.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.all().filter(status__exact='o').order_by('due_back')


class AuthorCreate(CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'catalog/author_create.html'


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'catalog/book_create.html'


class BookUpdate(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'catalog/book_create.html'


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')


class BookInstanceCreate(CreateView):
    model = BookInstance
    fields = '__all__'
    success_url = reverse_lazy('bookInstance-create')


class BookInstanceUpdate(UpdateView):
    model = BookInstance
    fields = ['id', 'imprint', 'due_back', 'status', 'borrower']


class BookInstanceDelete(DeleteView):
    model = BookInstance
    success_url = reverse_lazy('books')


from django.shortcuts import get_object_or_404, redirect
from catalog.models import BookInstance


def return_book(request, id):
    book_instance = get_object_or_404(BookInstance, id=id)

    # Установите статус книги на "d" (возвращена)
    book_instance.status = 'a'
    book_instance.borrower = None
    book_instance.due_back = None
    book_instance.save()

    return redirect('all-borrowed')


def get_book(request, id):
    if request.method == 'POST':
        copy_id = BookInstance.objects.get(id=id)
        copy_id.status = 'o'
        copy_id.borrower = request.user
        id = copy_id.book.id
        copy_id.due_back = datetime.date.today() + datetime.timedelta(weeks=3)
        copy_id.save()
        return redirect('book-detail', id=id)


from django.contrib.auth.forms import UserCreationForm


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        # Проверяем правильность введенных данных
        if form.is_valid():
            return super().form_valid(form)
        else:
            # Если есть ошибки, передаем их в контекст представления
            context = self.get_context_data(form=form)
            return self.render_to_response(context)
