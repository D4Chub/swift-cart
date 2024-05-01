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
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


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

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            if created:
                return Response({'message': 'Cart created successfully.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Cart already exists for this user.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'User is not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        

class CartItemAPIView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(cart__user=user)

