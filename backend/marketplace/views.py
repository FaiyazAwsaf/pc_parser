from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Q
from .models import Product, Order, Chat, Message, SellerRating
from .serializers import (
    ProductSerializer, ProductCreateSerializer, OrderSerializer,
    ChatSerializer, MessageSerializer, SellerRatingSerializer
)
from .pagination import CursorPagination

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = CursorPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'condition', 'age', 'warranty', 'box_accessories', 
                       'price_type', 'availability', 'brand', 'compatibility', 'performance_tier']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)
        
        # Price range filtering
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        print(f"Price filtering - min_price: {min_price}, max_price: {max_price}")
        
        if min_price:
            try:
                min_price_val = float(min_price)
                queryset = queryset.filter(price__gte=min_price_val)
                print(f"Applied min_price filter: {min_price_val}")
            except (ValueError, TypeError):
                print(f"Invalid min_price value: {min_price}")
                
        if max_price:
            try:
                max_price_val = float(max_price)
                queryset = queryset.filter(price__lte=max_price_val)
                print(f"Applied max_price filter: {max_price_val}")
            except (ValueError, TypeError):
                print(f"Invalid max_price value: {max_price}")
        
        # Debug: Print the final query and count
        print(f"Final queryset count: {queryset.count()}")
        if queryset.exists():
            prices = list(queryset.values_list('price', flat=True)[:10])
            print(f"Sample prices from results: {prices}")
        
        # Additional filters that require custom logic
        seller_rating = self.request.query_params.get('seller_rating')
        distance = self.request.query_params.get('distance')
        listing_age = self.request.query_params.get('listing_age')
        
        # Note: These filters would require additional implementation
        # For now, they are placeholders for future enhancement
        # seller_rating would need a rating system
        # distance would need location data
        # listing_age can be implemented with date filtering
        
        if listing_age:
            from datetime import datetime, timedelta
            if listing_age == 'today':
                queryset = queryset.filter(created_at__date=datetime.now().date())
            elif listing_age == 'week':
                week_ago = datetime.now() - timedelta(days=7)
                queryset = queryset.filter(created_at__gte=week_ago)
            elif listing_age == 'month':
                month_ago = datetime.now() - timedelta(days=30)
                queryset = queryset.filter(created_at__gte=month_ago)
            
        return queryset

class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    queryset = Product.objects.filter(is_available=True)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class MyProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)

class MyProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CursorPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category', 'brand']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)

class MyOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(product__seller=self.request.user)

class ChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Chat.objects.filter(
            Q(buyer=self.request.user) | Q(seller=self.request.user)
        )

class ChatDetailView(generics.RetrieveAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Chat.objects.filter(
            Q(buyer=self.request.user) | Q(seller=self.request.user)
        )

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        chat = Chat.objects.get(
            Q(id=chat_id) & (Q(buyer=self.request.user) | Q(seller=self.request.user))
        )
        return Message.objects.filter(chat=chat)

class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        chat_id = self.kwargs['chat_id']
        chat = Chat.objects.get(
            Q(id=chat_id) & (Q(buyer=self.request.user) | Q(seller=self.request.user))
        )
        serializer.save(sender=self.request.user, chat=chat)

class CreateChatView(generics.CreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            
            # Don't allow seller to chat with themselves
            if product.seller == request.user:
                return Response(
                    {'error': 'You cannot chat about your own product'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get or create chat
            chat, created = Chat.objects.get_or_create(
                product=product,
                buyer=request.user,
                seller=product.seller
            )
            
            serializer = ChatSerializer(chat)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class ProductCategoriesView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        """Get all available product categories"""
        categories = [choice[0] for choice in Product.CATEGORY_CHOICES]
        return Response({'categories': categories})

class ProductConditionsView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        """Get all available product conditions"""
        conditions = [choice[0] for choice in Product.CONDITION_CHOICES]
        return Response({'conditions': conditions})

class SearchSuggestionsView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        """Get search suggestions based on query"""
        query = request.query_params.get('q', '').strip()
        
        if len(query) < 2:
            return Response({'suggestions': []})
        
        # Limit to 10 suggestions for performance
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_available=True
        ).values('name', 'category', 'brand').distinct()[:10]
        
        suggestions = []
        seen = set()
        
        for product in products:
            # Add product name suggestions
            name = product['name']
            if name not in seen and query.lower() in name.lower():
                suggestions.append({
                    'text': name,
                    'type': 'product',
                    'category': product['category'],
                    'brand': product['brand']
                })
                seen.add(name)
        
        # Add brand suggestions
        brands = Product.objects.filter(
            brand__icontains=query,
            is_available=True
        ).values_list('brand', flat=True).distinct()[:5]
        
        for brand in brands:
            brand_display = dict(Product.BRAND_CHOICES).get(brand, brand)
            if brand_display not in seen:
                suggestions.append({
                    'text': brand_display,
                    'type': 'brand',
                    'value': brand
                })
                seen.add(brand_display)
        
        # Add category suggestions
        categories = Product.objects.filter(
            category__icontains=query,
            is_available=True
        ).values_list('category', flat=True).distinct()[:3]
        
        for category in categories:
            if category not in seen:
                suggestions.append({
                    'text': category,
                    'type': 'category',
                    'value': category
                })
                seen.add(category)
        
        return Response({'suggestions': suggestions[:10]})

class SellerRatingCreateView(generics.GenericAPIView):
    serializer_class = SellerRatingSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, seller_id):
        print(f"SellerRatingCreateView called with seller_id: {seller_id}")
        print(f"Request user: {request.user}")
        print(f"Request data: {request.data}")
        
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            seller = User.objects.get(id=seller_id)
            print(f"Found seller: {seller}")
            
            # Don't allow seller to rate themselves
            if seller == request.user:
                print("User trying to rate themselves")
                return Response(
                    {'error': 'You cannot rate yourself'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if user has already rated this seller
            existing_rating = SellerRating.objects.filter(
                seller=seller, 
                rater=request.user
            ).first()
            print(f"Existing rating: {existing_rating}")
            
            if existing_rating:
                # Update existing rating
                print("Updating existing rating")
                serializer = SellerRatingSerializer(
                    existing_rating, 
                    data=request.data, 
                    partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    print("Rating updated successfully")
                    return Response(serializer.data, status=status.HTTP_200_OK)
                print(f"Serializer errors (update): {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Create new rating
                print("Creating new rating")
                serializer = SellerRatingSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(rater=request.user, seller=seller)
                    print("Rating created successfully")
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                print(f"Serializer errors (create): {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except User.DoesNotExist:
            print(f"Seller with id {seller_id} not found")
            return Response(
                {'error': 'Seller not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SellerRatingListView(generics.ListAPIView):
    serializer_class = SellerRatingSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        seller_id = self.kwargs['seller_id']
        return SellerRating.objects.filter(seller_id=seller_id)

class UserStatsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        total_products = Product.objects.filter(seller=user).count()
        completed_sales = Order.objects.filter(
            product__seller=user, 
            status='completed'
        )
        total_sold = completed_sales.count()
        total_revenue = sum(sale.total_price for sale in completed_sales)
        active_chats = Chat.objects.filter(
            Q(buyer=user) | Q(seller=user)
        ).count()
        
        return Response({
            'total_products': total_products,
            'total_sold': total_sold,
            'total_revenue': float(total_revenue),
            'active_chats': active_chats
        })
