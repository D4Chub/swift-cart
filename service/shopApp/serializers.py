from  rest_framework import serializers
from .models import Cart, Product, CartItem, Category


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(source='category.name')

    class Meta:
        model = Product
        fields = ['id', 'name', 'regular_price', 'discount_price', 'stock', 'description', 'category']