from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    TopProductsView,
    ProductCategoryCreateView,
    OrderCreateView
)

app_name = "products"
urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('<int:pk>', ProductDetailView.as_view(), name='product-details'),
    path('<int:pk>/update',
         ProductUpdateView.as_view(), name='product-update'),
    path('create', ProductCreateView.as_view(), name='product-create'),
    path('top-ordered-products/',
         TopProductsView.as_view(), name='product-top'),
    path('<int:pk>/delete',
         ProductDeleteView.as_view(), name='product-delete'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
#     path('orders/confirmation/', OrderConfirmationView.as_view(), name='order-confirmation'),
    path('category/create', ProductCategoryCreateView.as_view(), name='category-create')
]
