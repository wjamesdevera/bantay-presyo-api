from django.contrib import admin
from .models import Category, Commodity, CommodityPrices

# Register your models here.
admin.site.register(Category)
admin.site.register(Commodity)
admin.site.register(CommodityPrices)
