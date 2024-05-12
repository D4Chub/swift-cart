from typing import List
from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from shopApp.models import Product
from shopApp.serializers import (
    ProductSerializer,
    ProductPriceSerializer,
    CartSerializer,
    OrderSerializer
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from services.services import (
    get_products_by_category,
    process_order,
    calculate_total_price,
    save_cart
)


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductAPIView(viewsets.ModelViewSet):
    """GET: Отображение всех товаров"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    permission_classes = [IsAuthenticated]


class ProductDetailAPIView(APIView):
    """GET: Отображение конкретного товара по его ID"""

    permission_classes = [IsAuthenticated]
    
    def get(self, pk: int) -> Response:
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    

class ProductPriceAPIView(viewsets.ModelViewSet):
    """GET: Отображение количества товаров на складе и цены со скидкой и без"""

    queryset = Product.objects.all()
    serializer_class = ProductPriceSerializer
    permission_classes = [IsAuthenticated]


class ProductByCategoryAPIView(generics.ListAPIView):
    """GET: Отображение товаров по id их категории и подкатегории"""
    
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> List[Product]: # type: ignore
        category_id = self.kwargs['id']
        products = get_products_by_category(category_id)
        return products


class IsOwnUser(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj) -> bool: # type: ignore
        # Разрешено доступ только для владельца объекта
        return obj.user == request.user
    

class CartAPIView(generics.CreateAPIView):
    """POST: Добавление товара в корзину"""

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsOwnUser]
    
    def perform_create(self, serializer):
        calculate_total_price(serializer)
        save_cart(serializer, user=self.request.user)
        

class OrderAPIView(APIView):
    """POST: Оформление заказа и отправка чека на почту"""

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnUser]

    def post(self, request, format=None) -> Response:
        user = request.user
        user_cart = user.cart_set.filter(status=True).first()
        if user_cart is None:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        message = process_order(user, user_cart)
        
        return Response({'message': message}, status=status.HTTP_201_CREATED)
    
