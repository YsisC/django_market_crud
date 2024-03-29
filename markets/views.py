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
# views.py

from django.http import JsonResponse
from django.db import connection

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

#   SELECT
#         p.Ean,
#         MAX(p.name) AS nombre_producto,
#         ARRAY_AGG(
#     JSON_BUILD_OBJECT(
#       'producto', p.name,
#       'mercado', m.name,
#       'precio_normal', pr.normal_price,
#       'precio_descuento', pr.discount_price
#     )
#      ) AS datos_query,
#      COUNT(DISTINCT m.id) AS cantidad_markets,
#     MAX(pr.normal_price) - MIN(pr.normal_price) AS rango_precios
#     FROM
    
#     markets_product p
#     JOIN
#     markets_price pr ON p.id = pr.product_id
#     JOIN
#     markets_market m ON pr.market_id = m.id
#     GROUP BY
#     p.Ean


def get_product_data(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                p.Ean,
                MAX(p.name) AS nombre_producto,
                json_group_array(
                    json_object(
                        'producto', p.name,
                        'mercado', m.name,
                        'precio_normal', pr.normal_price,
                        'precio_descuento', pr.discount_price
                    )
                ) AS datos_query,
                COUNT(DISTINCT m.id) AS cantidad_markets,
                MAX(pr.normal_price) - MIN(pr.normal_price) AS rango_precios
            FROM
                markets_product p
                JOIN markets_price pr ON p.id = pr.product_id
                JOIN markets_market m ON pr.market_id = m.id
            GROUP BY
                p.Ean
        """)
        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return JsonResponse({'products': data})




def group_products(data):
    productos_agrupados = {}

    for producto in data:
        ean = producto['Ean']
        nombre_producto = producto['nombre_producto']
        datos_query = producto['datos_query']
        market_id = producto['market']
        mayor_precio = producto['rango_precios']['mayor']
        menor_precio = producto['rango_precios']['menor']

        if ean not in productos_agrupados:
            productos_agrupados[ean] = {
                'nombre_producto': nombre_producto,
                'datos_query': [],
                'cantidad_markets': set(),
                'rango_precios': {'mayor': float('-inf'), 'menor': float('inf')}
            }

        productos_agrupados[ean]['datos_query'].extend(datos_query)
        productos_agrupados[ean]['cantidad_markets'].add(market_id)

        if mayor_precio > productos_agrupados[ean]['rango_precios']['mayor']:
            productos_agrupados[ean]['rango_precios']['mayor'] = mayor_precio
        if menor_precio < productos_agrupados[ean]['rango_precios']['menor']:
            productos_agrupados[ean]['rango_precios']['menor'] = menor_precio

    for ean, producto_info in productos_agrupados.items():
        producto_info['cantidad_markets'] = len(producto_info['cantidad_markets'])
        # Calcula el rango de precios en el formato deseado
        producto_info['rango_precios'] = f"{producto_info['rango_precios']['mayor']} - {producto_info['rango_precios']['menor']}"

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


