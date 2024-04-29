from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')
    
    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.product.name} in {self.cart}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


    def save(self, *args, **kwargs):
        if self.product.stock < self.amount:
            raise ValueError('Not enough stock for this product')
        
        self.total_price = self.product.regular_price * self.amount
        
        self.product.stock -= self.amount
        self.product.save()
        
        super(Order, self).save(*args, **kwargs)


    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    

class CartOrder(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.total_price += self.product.regular_price * self.quantity
        self.total_price.save()

        if self.product.stock >= self.quantity:
            self.product.stock -= self.quantity
            self.product.save()
        else:
            raise ValueError('Not enough stock for this product')

