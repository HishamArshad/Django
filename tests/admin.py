from django.contrib import admin
from .models import Musician, Album
from .models import Category, Product, Cart, CartItem, Order, OrderItem

admin.site.register(Musician)
admin.site.register(Album)
 


# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'category', 'created_at', 'updated_at')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

# Cart Admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__username',)

# CartItem Admin
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')
    list_filter = ('cart', 'product')

# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')

# OrderItem Admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')
    list_filter = ('order', 'product')
