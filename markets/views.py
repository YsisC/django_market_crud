from rest_framework import viewsets
from django.db import models
from rest_framework.response import Response
from .models import Market, Product, Price, ProductManager
from .serializer import MarketSerializer, ProductSerializer, PriceSerializer 
# ProductLastActivePriceSerializer



class LastActiveProductView(viewsets.ReadOnlyModelViewSet): 
    queryset= Product.objects.get_products_with_last_active_price()
    serializer_class = ProductSerializer
    
class MarketViewSet(viewsets.ModelViewSet):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer


