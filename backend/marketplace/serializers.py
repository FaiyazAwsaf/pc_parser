from rest_framework import serializers
from .models import Product, Order, Chat, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.username', read_only=True)
    seller_email = serializers.CharField(source='seller.email', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category', 'condition', 'description', 
                 'image', 'is_available', 'created_at', 'updated_at', 'seller', 
                 'seller_name', 'seller_email', 'age', 'warranty', 'box_accessories',
                 'price_type', 'availability', 'brand', 'compatibility', 'performance_tier']
        read_only_fields = ['seller', 'created_at', 'updated_at']

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'condition', 'description', 'image',
                 'age', 'warranty', 'box_accessories', 'price_type', 'availability',
                 'brand', 'compatibility', 'performance_tier']

class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    seller_name = serializers.CharField(source='product.seller.username', read_only=True)
    buyer_name = serializers.CharField(source='buyer.username', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'product', 'product_name', 'seller_name', 'buyer_name', 
                 'status', 'quantity', 'total_price', 'shipping_address', 
                 'created_at', 'updated_at']
        read_only_fields = ['buyer', 'total_price', 'created_at', 'updated_at']

class ChatSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    buyer_name = serializers.CharField(source='buyer.username', read_only=True)
    seller_name = serializers.CharField(source='seller.username', read_only=True)
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Chat
        fields = ['id', 'product', 'product_name', 'buyer', 'buyer_name', 
                 'seller', 'seller_name', 'created_at', 'last_message']
        read_only_fields = ['created_at']
    
    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return {
                'content': last_message.content,
                'sender': last_message.sender.username,
                'created_at': last_message.created_at
            }
        return None

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'sender_name', 'content', 
                 'created_at', 'is_read']
        read_only_fields = ['chat', 'sender', 'created_at']
