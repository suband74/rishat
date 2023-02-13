from rest_framework import serializers

from .models import Product, Order


class ProductSrlz(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class OrderSrlz(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"