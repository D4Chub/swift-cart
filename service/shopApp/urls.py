from django.urls import path, include
from rest_framework import routers
from .views import * 


urlpatterns = [
    path('products/', ProductAPIView.as_view({'get': 'list'})), 
    path('products/<int:pk>/', ProductDetailAPIView.as_view()), 
    path('categories/<int:id>/products/', ProductByCategoryAPIView.as_view(), name='products-by-category'),
    path('products/stock/', ProductPriceAPIView.as_view({'get': 'list'})),
    path('cart/add/', CartItemAPIView.as_view(), name='add-to-cart'),
    path('cart/', CartAPIView.as_view(), name='checkout'),
    path('auth/', include('rest_framework.urls')),

]

