from django.urls import path, include
from rest_framework import routers
from .views import * 


urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('products/', ProductAPIView.as_view({'get': 'list'})), 
    path('products/<int:pk>/', ProductDetailAPIView.as_view()), 
    path('categories/<int:id>/products/', ProductByCategoryAPIView.as_view(), name='products-by-category'),
    path('products/stock/', ProductPriceAPIView.as_view({'get': 'list'})),
    
    path('add/cart/', CartAPIView.as_view(), name='add-cart'),
    path('cart/item/', CartAPIView.as_view(), name='add-items-in-cart'),

]
