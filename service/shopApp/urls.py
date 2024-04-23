from django.urls import path, include
from rest_framework import routers
from .views import * 


urlpatterns = [
    path('products/', ProductAPIView.as_view({'get': 'list'})),
    path('products/<int:pk>/', ProductDetailAPIView.as_view()),

]

