from django.urls import path
from . import views

urlpatterns = [
    # Product URLs
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/create/', views.ProductCreateView.as_view(), name='product-create'),
    path('products/my/', views.MyProductsView.as_view(), name='my-products'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    
    # Order URLs
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/create/', views.OrderCreateView.as_view(), name='order-create'),
    path('orders/my/', views.MyOrdersView.as_view(), name='my-orders'),
    
    # Chat URLs
    path('chats/', views.ChatListView.as_view(), name='chat-list'),
    path('chats/<int:pk>/', views.ChatDetailView.as_view(), name='chat-detail'),
    path('chats/<int:chat_id>/messages/', views.MessageListView.as_view(), name='message-list'),
    path('chats/<int:chat_id>/messages/create/', views.MessageCreateView.as_view(), name='message-create'),
    path('products/<int:product_id>/chat/', views.CreateChatView.as_view(), name='create-chat'),
    
    # Utility URLs
    path('categories/', views.ProductCategoriesView.as_view(), name='product-categories'),
    path('conditions/', views.ProductConditionsView.as_view(), name='product-conditions'),
    path('search-suggestions/', views.SearchSuggestionsView.as_view(), name='search-suggestions'),
]
