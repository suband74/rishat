from rest_framework import routers
from django.urls import path, include

from .api import ProductViewSet, OrderViewSet


router = routers.DefaultRouter()

router.register("product", ProductViewSet, basename="product")
router.register("order", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls), name="api"),
]