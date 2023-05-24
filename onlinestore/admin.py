from django.contrib import admin
from .models import Products, Order

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_ordered')  # Display user and is_ordered fields
    list_filter = ('user',)  # Add a filter for user

    def get_queryset(self, request):
        # Override the default queryset to include the desired filtering
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('user')
        return queryset
