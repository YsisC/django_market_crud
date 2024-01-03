from django.urls import path, include
from rest_framework import routers
from .views import MarketViewSet, ProductViewSet, PriceViewSet, LastActiveProductView

router = routers.DefaultRouter()
router.register(r'markets', MarketViewSet)
router.register(r'products', ProductViewSet)
router.register(r'prices', PriceViewSet)
# router.register(r'products/last_active_price', ProductLastActivePriceViewSet)


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/products/last_active/', LastActiveProductView.as_view({'get': 'list'}), name='last_active_products'),

]
