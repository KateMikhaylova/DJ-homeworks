from django.http import HttpResponse
from django.shortcuts import render, reverse
import datetime
from os import listdir


def home_view(request):
    template_name = 'app/home.html'
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    current_time = datetime.datetime.now().strftime('%A, %B %d, %Y, %H:%M:%S')
    msg = f'Текущее время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    files = listdir('.')
    template_name = 'app/files.html'
    context = {'files': files}
    return render(request, template_name, context)

    raise NotImplemented
