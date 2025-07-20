from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Commodity, Category
from .serializers import CommoditySerializer, CategorySerializer


# Create your views here.
@api_view(["GET"])
def list_commodities(request):
    commodities = Commodity.objects.all()
    serializer = CommoditySerializer(
        commodities, many=True, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def list_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(
        categories, many=True, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def view_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def view_commodity(request, pk):
    commodity = Commodity.objects.get(pk)
    serializer = CommoditySerializer(
        commodity, many=True, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)
