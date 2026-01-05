from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from example_api.views import ExampleApiListView, ExampleApiDetailView
from categories.views import CategoryListView
from products.views import ProductCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/examples/', ExampleApiListView.as_view(), name='example-list'),
    path('api/categories/', CategoryListView.as_view(), name='category-list'),
    path('api/product/create/', ProductCreateView.as_view(), name='product-create'),
    path('api/examples/<uuid:id>/', ExampleApiDetailView.as_view(), name='example-detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)