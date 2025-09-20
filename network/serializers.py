from rest_framework import serializers
from .models import Product, NetworkLink

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class NetworkLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkLink
        fields = (
            'id', 'name', 'level', 'email', 'country', 'city', 'street',
            'house_number', 'products', 'supplier', 'debt', 'created_at'
        )
        # Запрещаем обновление поля 'debt' через API
        read_only_fields = ('debt', 'created_at')
