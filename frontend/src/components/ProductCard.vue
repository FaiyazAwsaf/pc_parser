<template>
  <div class="product-card">
    <div class="product-image">
      <img 
        :src="product.image || '/placeholder-product.jpg'" 
        :alt="product.name"
        @error="handleImageError"
      />
      <div class="product-condition">{{ product.condition }}</div>
    </div>
    
    <div class="product-info">
      <h3 class="product-name">{{ product.name }}</h3>
      <p class="product-category">{{ product.category }}</p>
      <p class="product-price">৳{{ formatPrice(product.price) }}</p>
      <p class="product-seller">Seller: {{ product.seller_name }}</p>
      
      <div class="product-description">
        {{ truncateDescription(product.description) }}
      </div>
      
      <div class="product-actions">
        <button 
          @click="$emit('order', product)" 
          class="order-btn"
          :disabled="!product.is_available"
        >
          {{ product.is_available ? 'Order' : 'Sold Out' }}
        </button>
        <button 
          @click="$emit('chat', product)" 
          class="chat-btn"
        >
          Chat
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductCard',
  props: {
    product: {
      type: Object,
      required: true
    }
  },
  emits: ['order', 'chat'],
  methods: {
    formatPrice(price) {
      return new Intl.NumberFormat('en-BD').format(price)
    },
    
    truncateDescription(description) {
      if (description.length > 100) {
        return description.substring(0, 100) + '...'
      }
      return description
    },
    
    handleImageError(event) {
      event.target.src = '/placeholder-product.jpg'
    }
  }
}
</script>

<style scoped>
.product-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
  width: 250px;
  margin-bottom: 20px;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.product-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-condition {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.product-info {
  padding: 16px;
}

.product-name {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
  line-height: 1.3;
}

.product-category {
  color: #666;
  font-size: 14px;
  margin: 0 0 8px 0;
  text-transform: uppercase;
  font-weight: 500;
}

.product-price {
  font-size: 20px;
  font-weight: 700;
  color: #007bff;
  margin: 0 0 8px 0;
}

.product-seller {
  color: #666;
  font-size: 13px;
  margin: 0 0 12px 0;
}

.product-description {
  color: #555;
  font-size: 14px;
  line-height: 1.4;
  margin-bottom: 16px;
  min-height: 40px;
}

.product-actions {
  display: flex;
  gap: 8px;
}

.order-btn, .chat-btn {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.order-btn {
  background: #28a745;
  color: white;
}

.order-btn:hover:not(:disabled) {
  background: #218838;
}

.order-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.chat-btn {
  background: #007bff;
  color: white;
}

.chat-btn:hover {
  background: #0056b3;
}

@media (max-width: 768px) {
  .product-card {
    width: 100%;
    max-width: 300px;
  }
}
</style>
