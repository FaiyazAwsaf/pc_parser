from rest_framework import serializers
from .models import ComponentCategory, Manufacturer, Component, ComponentPrice, PriceHistory

class ComponentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentCategory
        fields = ['id', 'name', 'slug', 'description']

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'slug', 'logo', 'website']

class ComponentPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentPrice
        fields = ['id', 'vendor_name', 'vendor_url', 'price', 'currency', 
                 'is_available', 'is_on_sale', 'original_price', 'last_checked']

class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ['id', 'vendor_name', 'price', 'currency', 'recorded_at']

class ComponentListSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer(read_only=True)
    category = ComponentCategorySerializer(read_only=True)
    lowest_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Component
        fields = ['id', 'name', 'slug', 'manufacturer', 'category', 
                 'model_number', 'image', 'lowest_price']
    
    def get_lowest_price(self, obj):
        # Get the lowest available price for this component
        price = obj.prices.filter(is_available=True).order_by('price').first()
        if price:
            return {
                'price': price.price,
                'currency': price.currency,
                'vendor_name': price.vendor_name
            }
        return None

class ComponentDetailSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer(read_only=True)
    category = ComponentCategorySerializer(read_only=True)
    prices = ComponentPriceSerializer(many=True, read_only=True)
    price_history = serializers.SerializerMethodField()
    
    class Meta:
        model = Component
        fields = ['id', 'name', 'slug', 'manufacturer', 'category', 
                 'model_number', 'release_date', 'description', 
                 'specifications', 'image', 'prices', 'price_history']
    
    def get_price_history(self, obj):
        # Get the last 30 days of price history for charting
        history = obj.price_history.order_by('-recorded_at')[:30]
        return PriceHistorySerializer(history, many=True).data