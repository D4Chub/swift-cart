from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Модель юзера.
    
    Расширяет AbstractUser, добавляя поле email в
    качестве обязательного поля для аутентификации
    """
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


class Category(models.Model):
    """
    Модель с категориями товаров
    """
    name = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    """
    Модель для хранения товаров
    """
    name = models.CharField(max_length=255)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True
    )
    stock = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    def __str__(self):
        return str(self.name)


class Cart(models.Model):
    """
    Модель корзины юзера
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.product.name} - in cart [{self.quantity}]'


class Order(models.Model):
    """
    Модель оформления заказа
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
      