from django.db import models
from django.db.models import Subquery, OuterRef, Min, Max
from django.db import models

class Market(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class ProductManager(models.Manager):
    def get_products_with_last_active_price(self):
        subquery = Price.objects.filter(
            product_id=OuterRef('id'),
            active=True
        ).order_by('-create_date').values('normal_price')[:1]

        return self.annotate(
            last_active_price=Subquery(subquery),
            market_name=Subquery(subquery.values('market__name')[:1])  # Add this line
        ).filter(
            price__active=True,
            price__normal_price=OuterRef('last_active_price')
        ).values('id', 'name', 'SKU', 'Ean', 'market_name', 'last_active_price')


class Product(models.Model):
    name = models.CharField(max_length=255)
    SKU = models.CharField(max_length=50, unique=True)
    Ean = models.CharField(max_length=50, unique=True)

    objects = ProductManager()

    def __str__(self):
        return self.name

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    normal_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.market.name} - {self.normal_price}"
    
