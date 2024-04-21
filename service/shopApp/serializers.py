from  rest_framework import serializers
from .models import Cart, Product, CartItem, Category


class BaseModelSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)

    
        if not hasattr(self.Meta, 'fields'):
            self.Meta.fields = '__all__'


class CategorySerializer(BaseModelSerializer):
    class Meta:
        model = Category 

 
class CartItemSerializer(BaseModelSerializer):
    class Meta:
        model = CartItem


class CartSerializer(BaseModelSerializer):
    products = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['user', 'products']


class ProductSerializer(BaseModelSerializer):
    class Meta:
        model = Product