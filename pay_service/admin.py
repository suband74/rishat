from django.contrib import admin

from .models import Product, Order

@admin.register(Product)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "price")


@admin.register(Order)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "product_to_pay", "amount", "state")
