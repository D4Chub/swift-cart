from typing import List, Dict, Any
from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from .models import Product, Category, Cart, Order
from .serializers import ProductSerializer, ProductPriceSerializer, CartSerializer, OrderSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductAPIView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    permission_classes = [IsAuthenticated]


class ProductDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk: int, format=None) -> Response:
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    

class ProductPriceAPIView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductPriceSerializer
    permission_classes = [IsAuthenticated]


class ProductByCategoryAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> List[Product]:
        category_id = self.kwargs['id']

        def get_child_category(category: Category) -> List[Category]:
            child_categories = [category]

            for child in category.children.all():
                child_categories.extend(get_child_category(child))

            return child_categories
        
        try:
            category = Category.objects.get(id=category_id)
            categories = get_child_category(category=category)
        except Category.DoesNotExist:
            return []

        products = Product.objects.filter(category__in=categories)
        return products


class IsOwnUser(permissions.BasePermission):
    """Пользователь может просматривать только свои объекты."""
    
    def has_object_permission(self, request, view, obj):
        # Разрешено доступ только для владельца объекта
        return obj.user == request.user
    

class CartAPIView(generics.CreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsOwnUser]
    
    def perform_create(self, serializer) -> None:
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        total_price = product.discount_price * quantity
        serializer.save(total_price=total_price, user=self.request.user)
        

class OrderAPIView(APIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnUser]

    def post(self, request, format=None) -> Response:
        user = request.user
        user_cart: Cart = user.cart_set.filter(status=True).first()
        total_price: int = user_cart.product.discount_price * user_cart.quantity
        
        user_cart.product.stock -= user_cart.quantity
        user_cart.product.save()

        user_cart.status = False
        user_cart.save()
        
        message = f"Order placed successfully. Product: {user_cart.product} || Total price: {total_price}"

        return Response({'message': message}, status=status.HTTP_201_CREATED)
