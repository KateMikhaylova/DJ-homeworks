"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, register_converter
from datetime import datetime

from books.views import BookListView, date_view


class DateConverter:
    """
    Class for date converter
    attribures:
        regex: regular expression to identify date in url
        format: date format to YYYY-MM-DD
    """
    regex = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
    format = '%Y-%m-%d'

    def to_python(self, value: str) -> datetime:
        """
        Converts date string to datetime class
        :param value: string object
        :return: corresponding datetime object
        """
        return datetime.strptime(value, self.format)

    def to_url(self, value: datetime) -> str:
        """
        Converts datetime to string
        :param value: datetime object
        :return: corresponding string object
        """
        return value.strftime(self.format)


register_converter(DateConverter, 'date')

urlpatterns = [
    path('books/', BookListView.as_view(), name='books'),
    path('books/<date:date>/', date_view, name='date_books'),
    path('admin/', admin.site.urls),
]
