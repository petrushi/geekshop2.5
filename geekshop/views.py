from django.shortcuts import render

from basketapp.models import Basket
from mainapp.models import Product


def index(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    title = 'geekshop'
    products = Product.objects.all()[:4]

    context = {
        'products': products,
        'title': title,
        'basket': basket,
    }
    return render(request, 'geekshop/index.html', context=context)


def contacts(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    title= 'контакты'
    context = {
        'title': title,
        'basket': basket,
    }
    return render(request, 'geekshop/contact.html', context=context)
