from rest_framework import viewsets
from django.db import models
from django.db.models import Min, F
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import Market, Product, Price
from .serializer import MarketSerializer, ProductSerializer, PriceSerializer 
from rest_framework.views import APIView
from django.db.models import Min, F
from django.http import JsonResponse

def product_list(request):
    # Obtén los productos con su último menor precio activo
    products = Product.objects.annotate(last_active_price=Min('price__normal_price', filter=models.Q(price__active=True))) \
                              .filter(price__active=True, price__normal_price=F('last_active_price'))

    # Formatea los datos para la respuesta JSON
    product_data = []
    for product in products:
        # Obtén el último precio activo para el producto
        last_price = Price.objects.filter(product=product, active=True).order_by('-create_date').first()

        # Asegúrate de que haya un precio antes de acceder a market
        if last_price:
            product_data.append({
                'name': product.name,
                'SKU': product.SKU,
                'EAN': product.Ean,
                'market': last_price.market.name if last_price.market else None,
                'last_active_price': str(product.last_active_price),  # Convierte a cadena o formato deseado

            })

    return JsonResponse({'products': product_data})

def group_products(request):
    # Obtén los datos de la solicitud, ajusta según sea necesario
    # Obtener todos los datos de Product
    productos = Product.objects.all()

    # Obtener todos los datos de Price
    precios = Price.objects.all()

    # Obtener todos los datos de Market
    mercados = Market.objects.all()

    # Diccionario para almacenar los productos agrupados por Ean
    productos_agrupados = {}

    for producto in productos:
        ean = producto.Ean
        nombre_producto = producto.name
        precios_producto = precios.filter(product=producto)
        
        # Inicializar la entrada del diccionario si es la primera vez que se encuentra el Ean
        if ean not in productos_agrupados:
            productos_agrupados[ean] = {
                'nombre_producto': nombre_producto,
                'datos_query': [],
                'cantidad_markets': set(),
                'rango_precios': {'mayor': float('-inf'), 'menor': float('inf')}
            }

        # Agregar datos a la entrada del diccionario
        for precio_producto in precios_producto:
            market_id = precio_producto.market.id
            datos_query = f'Producto: {nombre_producto}, Mercado: {market_id}, Precio: {precio_producto.normal_price}'
            productos_agrupados[ean]['datos_query'].append(datos_query)
            productos_agrupados[ean]['cantidad_markets'].add(market_id)

            # Actualizar el rango de precios
            if precio_producto.normal_price > productos_agrupados[ean]['rango_precios']['mayor']:
                productos_agrupados[ean]['rango_precios']['mayor'] = precio_producto.normal_price
            if precio_producto.normal_price < productos_agrupados[ean]['rango_precios']['menor']:
                productos_agrupados[ean]['rango_precios']['menor'] = precio_producto.normal_price

    # Calcular la cantidad de markets diferentes
    for ean, producto_info in productos_agrupados.items():
        producto_info['cantidad_markets'] = len(producto_info['cantidad_markets'])

    return JsonResponse({'Ean': productos_agrupados})

class LastActivePriceMixin:
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter_params = {}

        for field in self.lookup_fields:
            if self.kwargs.get(field):
                filter_params[field] = self.kwargs[field]

        queryset = queryset.filter(price__active=True) \
            .annotate(last_active_price=Min('price__normal_price')) \
            .order_by('id')  # Ordena por el campo único de tu modelo, ajusta según sea necesario

        obj = get_object_or_404(queryset, **filter_params)
        self.check_object_permissions(self.request, obj)
        return obj

class ProductRetrieveView(LastActivePriceMixin, generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_fields = ['SKU', 'Ean']

class MarketViewSet(viewsets.ModelViewSet):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer


