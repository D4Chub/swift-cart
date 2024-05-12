from typing import List
from shopApp.models import Product, Category
from services.mail import send_mail

def get_products_by_category(category_id: int) -> List[Product]:
    """Отображает категорию и подкатегорию товаров"""

    def get_child_category(category: Category) -> List[Category]:
        child_categories = [category]
        for child in category.children.all():  # type: ignore
            child_categories.extend(get_child_category(child))
        return child_categories

    try:
        category = Category.objects.get(id=category_id)
        categories = get_child_category(category=category)
    except Category.DoesNotExist:
        return []

    products = Product.objects.filter(category__in=categories).all() 
    return list(products)
    
    
def process_order(user, user_cart) -> str:
    """Обрабатывает заказ пользователя и отправляет уведомление на почту"""

    total_price: float = user_cart.product.discount_price * user_cart.quantity        
    user_cart.product.stock -= user_cart.quantity
    user_cart.product.save()
    user_cart.status = False
    user_cart.save()

    email: str = user.email
    send_mail(receiver_email=email, product_name=user_cart.product.name, total_price=total_price, quantity=user_cart.quantity, name=user.username)

    message = f"Order placed successfully. Product: {user_cart.product} || Total price: {total_price}"

    return message


def calculate_total_price(serializer) -> None:
    product = serializer.validated_data['product']
    quantity = serializer.validated_data['quantity']
    total_price = product.discount_price * quantity
    serializer.validated_data['total_price'] = total_price

def save_cart(serializer, user) -> None:
    serializer.save(user=user)