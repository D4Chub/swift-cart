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
        fields = '__all__'
        

class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer()

    class Meta:
        model = CartItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем queryset для поля cart
        self.fields['cart'].queryset = self.context['request'].user.cart_set.all()




