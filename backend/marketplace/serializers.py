from rest_framework import serializers
from .models import Product, Order, Chat, Message, SellerRating
from django.contrib.auth import get_user_model

User = get_user_model()

class SellerRatingSerializer(serializers.ModelSerializer):
    rater_name = serializers.CharField(source='rater.username', read_only=True)
    seller_name = serializers.CharField(source='seller.username', read_only=True)
    
    class Meta:
        model = SellerRating
        fields = ['id', 'seller', 'rater', 'rater_name', 'seller_name', 'rating', 'review', 'created_at', 'updated_at']
        read_only_fields = ['seller', 'rater', 'created_at', 'updated_at']

class ProductSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.username', read_only=True)
    seller_email = serializers.CharField(source='seller.email', read_only=True)
    seller_rating = serializers.ReadOnlyField()
    seller_rating_count = serializers.ReadOnlyField()
    seller_rating_distribution = serializers.ReadOnlyField()
    user_seller_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category', 'condition', 'description', 
                 'image', 'is_available', 'created_at', 'updated_at', 'seller', 
                 'seller_name', 'seller_email', 'age', 'warranty', 'box_accessories',
                 'price_type', 'availability', 'brand', 'compatibility', 'performance_tier',
                 'seller_rating', 'seller_rating_count', 'seller_rating_distribution', 'user_seller_rating']
        read_only_fields = ['seller', 'created_at', 'updated_at']

    def get_user_seller_rating(self, obj):
        """Get the current user's rating for this seller"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                rating = obj.seller.seller_ratings.get(rater=request.user)
                return {
                    'rating': rating.rating,
                    'review': rating.review,
                    'created_at': rating.created_at
                }
            except SellerRating.DoesNotExist:
                return None
        return None

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'condition', 'description', 'image',
                 'age', 'warranty', 'box_accessories', 'price_type', 'availability',
                 'brand', 'compatibility', 'performance_tier']

class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_category = serializers.CharField(source='product.category', read_only=True)
    product_image = serializers.SerializerMethodField()
    seller_name = serializers.CharField(source='product.seller.username', read_only=True)
    buyer_name = serializers.CharField(source='buyer.username', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'product', 'product_name', 'product_category', 'product_image',
                 'seller_name', 'buyer_name', 'status', 'quantity', 'total_price', 
                 'shipping_address', 'created_at', 'updated_at']
        read_only_fields = ['buyer', 'total_price', 'created_at', 'updated_at']
    
    def get_product_image(self, obj):
        """Get product image URL, handling cases where image is None"""
        if obj.product.image:
            return obj.product.image.url
        return None

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
