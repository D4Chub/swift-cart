from rest_framework import serializers
from shopApp.models import (
    Product,
    Category,
    Cart,
    Order
)


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.
    """
    category = serializers.StringRelatedField(source='category.name')

    class Meta:
        model = Product
        fields = ['id', 'name', 'regular_price', 'discount_price', 'stock', 'description', 'category']


class ProductPriceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product с полями цен.
    """
    class Meta:
        model = Product
        fields = ['name', 'regular_price', 'discount_price', 'stock']


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category.
    """
    class Meta:
        model = Category
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Cart.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Cart

        fields = ['user', 'product', 'quantity']
        read_only_fields = ['total_price']


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Order.
    """
    class Meta:
        model = Order
        fields = ['cart']
        read_only_fields = ['total_price']
