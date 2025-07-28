from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import ComponentCategory, Manufacturer, Component, ComponentPrice, PriceHistory
from .serializers import (
    ComponentCategorySerializer,
    ManufacturerSerializer,
    ComponentListSerializer,
    ComponentDetailSerializer,
    ComponentPriceSerializer,
    PriceHistorySerializer
)

class ComponentCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ComponentCategory.objects.all()
    serializer_class = ComponentCategorySerializer
    lookup_field = 'slug'

class ManufacturerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    lookup_field = 'slug'

class ComponentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Component.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'manufacturer__slug']
    search_fields = ['name', 'model_number', 'description']
    ordering_fields = ['name', 'release_date']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ComponentDetailSerializer
        return ComponentListSerializer
    
    @action(detail=True, methods=['get'])
    def price_history(self, request, slug=None):
        """Get price history for a specific component"""
        component = self.get_object()
        history = component.price_history.order_by('-recorded_at')[:90]  # Last 90 days
        serializer = PriceHistorySerializer(history, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def compare(self, request):
        """Compare multiple components"""
        component_slugs = request.query_params.getlist('components')
        components = Component.objects.filter(slug__in=component_slugs, is_active=True)
        serializer = ComponentDetailSerializer(components, many=True)
        return Response(serializer.data)

class ComponentPriceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ComponentPrice.objects.filter(is_available=True)
    serializer_class = ComponentPriceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['component__slug', 'vendor_name', 'is_on_sale']
    ordering_fields = ['price', 'last_checked']
    ordering = ['price']
    
    @action(detail=False, methods=['get'])
    def best_deals(self, request):
        """Get the best deals (on sale items)"""
        deals = ComponentPrice.objects.filter(is_available=True, is_on_sale=True).order_by('price')[:20]
        serializer = self.get_serializer(deals, many=True)
        return Response(serializer.data)