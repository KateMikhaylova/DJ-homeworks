from django.shortcuts import render, HttpResponse
from django.views.generic import ListView
from .models import Book
from datetime import datetime


class BookListView(ListView):
    """
    Class to view full list of books
    attributes:
        model: refers to corresponding model in models package
        template_name: route to template used to render page with book list
    """
    model = Book
    template_name = 'books/books_list.html'


def date_view(request, date: datetime) -> HttpResponse:
    """
    Function to create webpage with books published on requested date
    :param request: users request
    :param date: publishing date
    :return:
    """
    books = Book.objects.filter(pub_date=date)

    dates = list(Book.objects.values('pub_date').distinct().order_by('pub_date'))
    current_date_index = dates.index({'pub_date': date.date()})

    if current_date_index != 0:
        previous_date_index = current_date_index - 1
        previous_date = dates[previous_date_index]['pub_date'].strftime('%Y-%m-%d')
    else:
        previous_date = None

    if current_date_index != (len(dates) - 1):
        next_date_index = current_date_index + 1
        next_date = dates[next_date_index]['pub_date'].strftime('%Y-%m-%d')
    else:
        next_date = None

    template = 'books/date_list.html'
    context = {'books': books,
               'previous_date': previous_date,
               'next_date': next_date}
    return render(request, template, context)
