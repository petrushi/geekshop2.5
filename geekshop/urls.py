from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from authapp import urls as authapp_urls
from mainapp import urls as mainapp_urls
from adminapp import urls as adminapp_urls
from basketapp import urls as basketapp_urls
from ordersapp import urls as ordersapp_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_staff/', include(adminapp_urls, namespace='admin_staff'), name='admin_staff'),

    path('auth/', include(authapp_urls, namespace='auth'), name='auth'),
    path('products/', include(mainapp_urls, namespace='products'), name='products'),
    path('basket/', include(basketapp_urls, namespace='basket'), name='basket'),
    path('order/', include(ordersapp_urls, namespace='order'), name='order'),
    
    path('', views.index, name='index'),
    path('contacts/', views.contacts, name='contacts'),
    path('', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns += [path('__debug__', include(debug_toolbar.urls))]