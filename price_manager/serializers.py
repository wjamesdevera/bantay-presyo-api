from rest_framework import serializers
from django.utils import timezone
from .models import Category, Commodity, CommodityPrices


# class BaseSerializer(serializers.Serializer):
#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         return {
#             'success': True,
#             'data': data,
#             'metadata': {
#                 'timestamp': timezone.now().isoformat(),
#                 'api_version': "1.0"
#             }
#         }


class CommoditySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Commodity
        fields = "__all__"


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
