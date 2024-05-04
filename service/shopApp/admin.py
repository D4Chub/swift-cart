from django.contrib import admin
from .models import *


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'total_price']
    list_display_links = ['user', 'product', 'quantity']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'regular_price', 'discount_price', 'stock']
    list_display_links = ['name', 'category', 'regular_price', 'discount_price', 'stock']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    list_display_links = ['name', 'parent']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['cart', 'total_price']
    list_display_links = ['cart', 'total_price']

