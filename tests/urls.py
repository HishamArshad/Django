from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryDetailView,
    ProductListCreateView,
    ProductDetailView,
    CartRetrieveView,
    CartItemCreateView,
    CartItemDeleteView,
    OrderListCreateView,
)

urlpatterns = [
    # Categories
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    # Products
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    # Cart
    path('cart/', CartRetrieveView.as_view(), name='cart-retrieve'),

    # Cart Items
    path('cart/items/', CartItemCreateView.as_view(), name='cartitem-create'),
    path('cart/items/<int:pk>/', CartItemDeleteView.as_view(), name='cartitem-delete'),

    # Orders
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
]
