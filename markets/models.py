# markets/models.py

from django.db import models

class Market(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    SKU = models.CharField(max_length=50, unique=True)
    Ean = models.CharField(max_length=50, unique=False)

    def last_active_price(self):
        last_price = self.price_set.filter(active=True).order_by('-create_date').first()
        return last_price.normal_price if last_price else None

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    normal_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.market.name} - {self.normal_price}"

