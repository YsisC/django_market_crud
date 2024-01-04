from rest_framework import serializers
from .models import Product, Price, Market
from django.db.models import OuterRef, Subquery



class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['normal_price', 'discount_price', 'active', 'create_date']

class ProductSerializer(serializers.ModelSerializer):
    last_active_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'SKU', 'Ean', 'last_active_price']

    def get_last_active_price(self, obj):
        return obj.last_active_price()

# class ProductSerializer(serializers.ModelSerializer):
#     last_active_price = PriceSerializer()
#     market_id = serializers.PrimaryKeyRelatedField(queryset=Market.objects.all(), source='market', write_only=True)
#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'SKU', 'Ean', 'market_id', 'las_active_price']

