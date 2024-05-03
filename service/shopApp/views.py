from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.db import transaction


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
    

class CartAPIView(generics.CreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        total_price = product.discount_price * quantity
        serializer.save(total_price=total_price, user=self.request.user) 


class OrderAPIView(APIView):
    serializer_class = OrderSerializer

    def post(self, request, format=None):
        # Получаем пользователя, для которого создается заказ
        user = request.user
        
        # Получаем корзину пользователя
        cart_items = Cart.objects.filter(user=user)
        
        # Вычисляем общую стоимость заказа на основе содержимого корзины
        total_price = sum(cart_item.product.discount_price * cart_item.quantity for cart_item in cart_items)
        
        cart_owner = Cart.objects.filter(user=user)

        # Создаем заказ
        order = Order.objects.create(cart=cart_owner, total_price=total_price)
        
        # Очищаем корзину пользователя
        cart_items.delete()
        
        return Response({'message': 'Order placed successfully'}, status=status.HTTP_201_CREATED)