from django.contrib import admin
from .models import Products, Order




@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'quantity', 'is_ordered')
    list_filter = ('is_ordered', 'user')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('product', 'user')
        return queryset

