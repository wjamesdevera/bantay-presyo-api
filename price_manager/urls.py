from django.urls import path
from .views import list_commodities, list_categories, view_category, view_commodity

urlpatterns = [
    path("categories/<int:pk>",
         view=view_category, name="category-detail"),
    path("commodities/<str:pk>",
         view=view_commodity, name="commodity-detail"),
    path("commodities/", view=list_commodities, name="list_commodities"),
    path("categories/", view=list_categories, name="list_categories"),
]
