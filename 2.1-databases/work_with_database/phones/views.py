from django.shortcuts import render, redirect
from .models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    phone_sort = request.GET.get('sort')
    if phone_sort == 'name':
        phones = Phone.objects.all().order_by('name')
    elif phone_sort == 'min_price':
        phones = Phone.objects.all().order_by('price')
    elif phone_sort == 'max_price':
        phones = Phone.objects.all().order_by('-price')
    else:
        phones = Phone.objects.all()
    template = 'catalog.html'
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    phone = Phone.objects.filter(slug=slug).first()

    template = 'product.html'
    context = {'phone': phone}
    return render(request, template, context)
