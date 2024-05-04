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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Cart

        fields = ['user', 'product', 'quantity']
        read_only_fields = ['total_price']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['cart']
        read_only_fields = ['total_price']
