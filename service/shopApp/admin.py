from django.contrib import admin
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'regular_price', 'discount_price']
    list_display_links = ['id', 'name', 'category']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent']
    list_display_links = ['id', 'name', 'parent']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user',]
    list_display_links = ['id', 'user']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity']
    list_display_links = ['id', 'cart', 'quantity', 'product']


 
