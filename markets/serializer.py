from rest_framework import serializers
from .models import Product, Price, Market

class ProductLastActivePriceSerializer(serializers.Serializer):
    name = serializers.CharField()
    EAN = serializers.CharField()
    SKU = serializers.CharField()
    last_active_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    market_name = serializers.CharField()


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'

class PriceSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    class Meta:
        model = Price
        fields = ['id', 'product', 'market', 'normal_price', 'discount_price', 'active', 'create_date']

class ProductSerializer(serializers.ModelSerializer):
    market_id = serializers.PrimaryKeyRelatedField(queryset=Market.objects.all(), source='market', write_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'SKU', 'Ean', 'market_id']

class ProductLastSerializer(serializers.ModelSerializer):
    market_id = serializers.PrimaryKeyRelatedField(queryset=Market.objects.all(), source='market', write_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'SKU', 'Ean', 'market_id']