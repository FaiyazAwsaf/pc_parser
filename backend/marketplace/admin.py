from django.contrib import admin
from .models import Product, Order, Chat, Message, ProductRating

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'seller', 'category', 'condition', 'price', 'is_available', 'created_at']
    list_filter = ['category', 'condition', 'is_available', 'created_at']
    search_fields = ['name', 'description', 'seller__username']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'buyer', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['product__name', 'buyer__username']
    readonly_fields = ['total_price', 'created_at', 'updated_at']

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'buyer', 'seller', 'created_at']
    search_fields = ['product__name', 'buyer__username', 'seller__username']
    readonly_fields = ['created_at']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat', 'sender', 'content', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['content', 'sender__username']
    readonly_fields = ['created_at']

@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['product__name', 'user__username', 'review']
    readonly_fields = ['created_at', 'updated_at']
