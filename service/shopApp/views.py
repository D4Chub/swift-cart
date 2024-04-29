from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Category, Product, Cart, CartItem
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class ProductPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductAPIView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination


class ProductDetailAPIView(APIView):
    def get(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    

class ProductPriceAPIView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductPriceSerializer


class CartAPIView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
        

class OrderAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ProductByCategoryAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer


    def get_queryset(self):
        category_id = self.kwargs['id']

        
        def get_child_category(category):

            child_categories = [category]

            for child in category.children.all():
                child_categories.extend(get_child_category(child))

            return child_categories
        
        try:
            category = Category.objects.get(id=category_id)
            categories = get_child_category(category=category)
        except Category.DoesNotExist:
            return Category.objects.none()
        

        products = Product.objects.filter(category__in=categories)

        return products
        

class CartOrderAPIView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(cart__user=user)

    def post(self, request, *args, **kwargs):
        user = request.user
        cart_items = CartItem.objects.filter(cart__user=user)

        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Создание заказа
        order = Order.objects.create(user=user)

        # Добавление товаров из корзины в заказ и уменьшение количества товаров на складе
        for cart_item in cart_items:
            product = cart_item.product
            if product.stock < cart_item.quantity:
                return Response({"error": f"Not enough stock for {product.name}"}, status=status.HTTP_400_BAD_REQUEST)

            # Создание пункта заказа
            order_item = order.orderitem_set.create(product=product, quantity=cart_item.quantity)

            # Уменьшение количества товаров на складе
            product.stock -= cart_item.quantity
            product.save()

        # Очистка корзины пользователя
        cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)