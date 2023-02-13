from rest_framework.viewsets import ModelViewSet

from .models import Product, Order
from .serializers import ProductSrlz, OrderSrlz


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSrlz


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSrlz
