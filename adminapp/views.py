from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from adminapp.forms import UserRegisterForm, ProductEditForm, ProductCategoryEditForm
from authapp.models import User
from ordersapp.models import Order

from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test

from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return User.objects.filter(is_active=True)


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'adminapp/user_create.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('admin_staff:users')


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        edit_form = UserRegisterForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()

            return HttpResponseRedirect(reverse('admin_staff:user_update', args=[edit_user.pk]))
    else:
        edit_form = UserRegisterForm(instance=edit_user)

    context = {
        'title': title,
        'update_form': edit_form,
    }

    return render(request, 'adminapp/user_update.html', context)


def user_delete(request, pk):
    title = 'пользователи/удаление'

    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        user.is_active = False
        user.save()

        return HttpResponseRedirect(reverse('admin_staff:users'))

    context = {
        'title': title,
        'user_to_delete': user,
    }

    return render(request, 'adminapp/user_delete.html', context)


def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    content = {
        'title': title,
        'objects': categories_list
    }

    return render(request, 'adminapp/categories.html', content)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_create.html'
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('admin_staff:categories')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/создание'
        return context


def category_update(request, pk):
    title = 'категория/редактирование'

    edit_category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        edit_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:category_update', args=[edit_category.pk]))
    else:
        edit_form = ProductCategoryEditForm(instance=edit_category)

    context = {'title': title,
               'form': edit_form,
               }

    return render(request, 'adminapp/category_create.html', context)


class CategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    context_object_name = 'category_to_delete'
    success_url = reverse_lazy('admin_staff:categories')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/product_list.html'

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs.get('pk'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        category = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        context.update({'category': category})

        return context


def products(request, pk):
    title = 'админка/категории продуктов'

    if pk == 0:
        categories = ProductCategory.objects.filter(is_active=True)
        context = {
            'title': title,
            'objects': categories,
        }

        return render(request, 'adminapp/categories.html', context)

    category = get_object_or_404(ProductCategory, pk=pk)
    products_category = Product.objects.filter(category__pk=pk)

    content = {
        'title': title,
        'category': category,
        'objects': products_category,
    }

    return render(request, 'adminapp/products.html', content)


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_create.html'
    form_class = ProductEditForm
    success_url = reverse_lazy('admin_staff:categories')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        category = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        context.update({'category': category})

        return context


def product_create(request, pk):
    title = 'продукты/создание'
    product_category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()

            return HttpResponseRedirect(reverse('admin_staff:products'), args=[pk])
    else:
        product_form = ProductEditForm(initial={'category': product_category})

    context = {
        'title': title,
        'update_form': product_form,
        'category': product_category
    }

    return render(request, 'adminapp/product_update.html', context)


def product_read(request, pk):
    product = get_object_or_404(Product, pk=pk)
    title = f'продукты/{product.name}'

    context = {
        'title': title,
        'product': product,
    }

    return render(request, 'adminapp/product_read.html', context)


def product_update(request, pk):

    product = get_object_or_404(Product, pk=pk)
    title = f'продукты/{product.name}'

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()

            return HttpResponseRedirect(reverse('admin_staff:product_update', args=[pk]))
    else:
        product_form = ProductEditForm(instance=product)

    context = {
        'title': title,
        'form': product_form,
        'category': product.category
    }

    return render(request, 'adminapp/product_update.html', context)


def product_delete(request, pk):
    title = 'продукты/удаление'

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.is_active = False
        product.save()

        return HttpResponseRedirect(reverse('admin_staff:products', args=[product.category.pk]))

    context = {
        'title': title,
        'product_to_delete': product,
        'category_pk': product.category.pk,
    }

    return render(request, 'adminapp/product_delete.html', context)


class OrderListView(ListView):
    model = Order
    template_name = 'adminapp/order_list.html'


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'adminapp/order_update.html'
    fields = ('status',)
    success_url = reverse_lazy('admin_staff:orders')