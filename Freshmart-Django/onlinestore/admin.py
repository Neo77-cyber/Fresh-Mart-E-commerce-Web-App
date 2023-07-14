from django.contrib import admin
from .models import Products, Order, OrderItem, CompletedOrderItem, Profile, Review, SellOnFreshMart






admin.site.register(Profile)
admin.site.register(Review)
admin.site.register(SellOnFreshMart)
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', )
    list_filter = ('user', )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('user')
        return queryset
    
@admin.register(OrderItem)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'is_ordered', 'date_ordered')
    list_filter = ('is_ordered', 'date_ordered', )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('product', 'order' )
        return queryset

@admin.register(CompletedOrderItem)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'is_ordered', 'date_ordered')
    list_filter = ('is_ordered', 'date_ordered',  )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('product', 'order')
        return queryset




