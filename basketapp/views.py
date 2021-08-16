from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache

from basketapp.models import Basket
from mainapp.models import Product

from django.contrib.auth.decorators import login_required


@never_cache
@login_required
def basket(request):
    title = 'Корзина'
    basket_items = []
    if request.user.is_authenticated:
        basket_items = Basket.objects.select_related()
    context = {
        'basket': basket_items,
        'title': title,
    }

    return render(request, 'basketapp/basket.html', context=context)


@login_required
def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

        context = {
            'basket': basket_items,
        }

        menu_result = render_to_string('geekshop/includes/inc_basket_preview.html', context)
        list_result = render_to_string('basketapp/includes/inc_basket_list.html', context)

        return JsonResponse({'menu_result': menu_result,
                             'list_result': list_result})