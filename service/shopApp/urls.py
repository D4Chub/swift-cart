from django.urls import path, include
from rest_framework import routers
from .views import * 


urlpatterns = [
    # Shows all products
    path('products/', ProductAPIView.as_view({'get': 'list'})), 
    
    # Shows the product by id
    path('products/<int:pk>/', ProductDetailAPIView.as_view()), 
    
    # Shows the product category and subcategory 
    path('categories/<int:id>/products/', ProductByCategoryAPIView.as_view(), name='products-by-category'),
    
    # Shows the product stock and regular-discount price
    path('products/stock/', ProductPriceAPIView.as_view({'get': 'list'})),
    
    # A request to add an item to the inventory
    path('cart/add/', CartAPIView.as_view()),
    
    # Request for an order
    path('order/', OrderAPIView.as_view()),

    #TODO request for an order proucts from user cart
]

    