from django.urls import path
import adminapp.views as adminapp
app_name = 'adminapp'

urlpatterns = [
    path('users/create/', adminapp.UserCreateView.as_view(), name='user_create'),
    path('users/read/', adminapp.UserListView.as_view(), name='users'),
    path('users/update/<int:pk>/', adminapp.user_update, name='user_update'),
    path('users/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),

    path('categories/create/', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    path('categories/read/', adminapp.categories, name='categories'),
    path('categories/update/<int:pk>/', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.CategoryDeleteView.as_view(), name='category_delete'),

    path('products/create/category/<int:pk>/', adminapp.ProductCreateView.as_view(), name='product_create'),
    path('products/read/category/<int:pk>/', adminapp.ProductsListView.as_view(), name='products'),
    path('products/read/<int:pk>/', adminapp.product_read, name='product_read'),
    path('products/update/<int:pk>/', adminapp.product_update, name='product_update'),
    path('products/delete/<int:pk>/', adminapp.product_delete, name='product_delete'),

    path('orders/read/', adminapp.OrderListView.as_view(), name='orders'),
    path('orders/update/<int:pk>/', adminapp.OrderUpdateView.as_view(), name='order_update'),
]
