from typing import List
from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from shopApp.models import Product, Category
from shopApp.serializers import ProductSerializer, ProductPriceSerializer, CartSerializer, OrderSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from shopApp.mail import send_mail



class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductAPIView(viewsets.ModelViewSet):
    """GET: Отображает все товары"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    permission_classes = [IsAuthenticated]


class ProductDetailAPIView(APIView):
    """GET: Отображает конкретный товар по его ID"""

    permission_classes = [IsAuthenticated]
    
    def get(self, pk: int) -> Response:
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    

class ProductPriceAPIView(viewsets.ModelViewSet):
    """GET: Отображает количество товаров на складе и цены со скидкой и без"""

    queryset = Product.objects.all()
    serializer_class = ProductPriceSerializer
    permission_classes = [IsAuthenticated]


class ProductByCategoryAPIView(generics.ListAPIView):
    """GET: Отображает категории и подкатегории"""
    
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
    
    def has_object_permission(self, request, obj) -> bool:
        # Разрешено доступ только для владельца объекта
        return obj.user == request.user
    

class CartAPIView(generics.CreateAPIView):
    """POST: Добавляет товар в коризну"""

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsOwnUser]
    
    def perform_create(self, serializer: CartSerializer) -> None:
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        total_price = product.discount_price * quantity
        serializer.save(total_price=total_price, user=self.request.user)
        

class OrderAPIView(APIView):
    """POST: Оформляет заказ и отправяет чек на почту"""

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnUser]

    def post(self, request, format=None) -> Response:
        user = request.user
        user_cart = user.cart_set.filter(status=True).first()
        if user_cart is None:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        total_price = user_cart.product.discount_price * user_cart.quantity        
        
        user_cart.product.stock -= user_cart.quantity
        user_cart.product.save()
        user_cart.status = False
        user_cart.save()
        
        email = user.email
        send_mail(receiver_email=email, product_name=user_cart.product.name, total_price=total_price, quantity=user_cart.quantity, name=user.username)
        
        message = f"Order placed successfully. Product: {user_cart.product} || Total price: {total_price}"

        return Response({'message': message}, status=status.HTTP_201_CREATED)
    
