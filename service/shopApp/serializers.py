from  rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(source='category.name')

    class Meta:
        model = Product
        fields = ['id', 'name', 'regular_price', 'discount_price', 'stock', 'description', 'category']


class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'regular_price', 'discount_price', 'stock']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    # product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['total_price',]