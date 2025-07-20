from django.db import models
import datetime
import uuid

from django.urls import reverse

# Create your models here.


class Category(models.Model):
    category_id = models.AutoField(
        primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category-detail", kwargs={"pk": self.pk})


class Commodity(models.Model):
    commodity_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    specification = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "commodity"
        verbose_name_plural = "commodities"

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def get_absolute_url(self):
        return reverse("commodity-detail", kwargs={"pk": self.pk})


class CommodityPrices(models.Model):
    commodity_price_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=11)
    date = models.DateField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "commodities_prices"
        verbose_name = "commodities_price"
        verbose_name_plural = "commodities_prices"

    def __str__(self):
        return f"{self.commodity} - {self.date}"
