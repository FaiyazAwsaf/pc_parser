<template>
  <div class="bg-white rounded-xl shadow-md overflow-hidden transition-all duration-200 hover:-translate-y-1 hover:shadow-xl w-64 mb-5">
    <div class="relative h-48 overflow-hidden">
      <img 
        :src="product.image || '/placeholder-product.jpg'" 
        :alt="product.name"
        @error="handleImageError"
        class="w-full h-full object-cover"
      />
      <div class="absolute top-2.5 right-2.5 bg-black bg-opacity-70 text-white px-2 py-1 rounded text-xs">
        {{ product.condition }}
      </div>
    </div>
    
    <div class="p-4">
      <h3 class="text-lg font-semibold text-gray-800 mb-2 leading-tight">{{ product.name }}</h3>
      <p class="text-gray-600 text-sm mb-2 uppercase font-medium tracking-wide">{{ product.category }}</p>
      <p class="text-xl font-bold text-blue-600 mb-2">৳{{ formatPrice(product.price) }}</p>
      <p class="text-gray-600 text-xs mb-3">Seller: {{ product.seller_name || 'Demo Seller' }}</p>
      
      <div class="text-gray-700 text-sm leading-relaxed mb-4 min-h-[2.5rem]">
        {{ truncateDescription(product.description) }}
      </div>
      
      <div class="flex gap-2">
        <button 
          @click="$emit('order', product)" 
          :disabled="!product.is_available"
          class="flex-1 py-2.5 px-3 rounded-md text-sm font-semibold transition-colors"
          :class="product.is_available !== false
            ? 'bg-green-500 text-white hover:bg-green-600' 
            : 'bg-gray-500 text-white cursor-not-allowed'"
        >
          {{ product.is_available !== false ? 'Order' : 'Sold Out' }}
        </button>
        <button 
          @click="$emit('chat', product)" 
          class="flex-1 py-2.5 px-3 bg-blue-500 text-white rounded-md text-sm font-semibold hover:bg-blue-600 transition-colors"
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
