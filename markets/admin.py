from django.contrib import admin
from .models import Price, Product, Market

admin.site.register(Product)
admin.site.register(Market)
admin.site.register(Price)