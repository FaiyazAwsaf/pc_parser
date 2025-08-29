<template>
  <div 
    class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300 h-full flex flex-col cursor-pointer"
    @click="handleCardClick"
  >
    <div class="relative">
      <img 
        :src="product.image || '/placeholder-product.jpg'" 
        :alt="product.name"
        @error="handleImageError"
        class="w-full h-48 object-contain bg-gray-100 p-4"
      />
      <span 
        class="absolute top-2 right-2 bg-blue-500 text-white text-xs font-bold px-2 py-1 rounded-full"
      >
        {{ product.condition }}
      </span>
    </div>
    
    <div class="p-4 flex flex-col flex-1">
      <div class="flex items-center justify-between mb-2">
        <span class="text-xs text-gray-500">{{ product.category }}</span>
        <span class="text-xs font-medium text-green-600">{{ product.seller_name || 'Demo Seller' }}</span>
      </div>
      
      <h3 class="text-lg font-semibold text-gray-800 mb-1 truncate">{{ product.name }}</h3>
      
      <!-- Seller Rating Display -->
      <div class="mb-2">
        <StarRating 
          :modelValue="product.seller_rating || 0"
          :count="product.seller_rating_count || 0"
          :interactive="false"
          :showText="true"
        />
      </div>
      
      <div class="flex-1 mb-3">
        <p class="text-sm text-gray-600 h-10 overflow-hidden">{{ truncateDescription(product.description) }}</p>
      </div>
      
      <div class="flex justify-between items-end mt-auto">
        <div>
          <p class="text-sm text-gray-500">Price:</p>
          <p class="text-xl font-bold text-blue-700">৳{{ formatPrice(product.price) }}</p>
        </div>
        
        <div class="flex space-x-2">
          <button 
            @click.stop="$emit('order', product)" 
            :disabled="!product.is_available"
            class="px-3 py-1 text-sm rounded transition"
            :class="product.is_available !== false
              ? 'bg-green-600 text-white hover:bg-green-700' 
              : 'bg-gray-400 text-white cursor-not-allowed'"
          >
            {{ product.is_available !== false ? 'Order' : 'Sold Out' }}
          </button>
          <button 
            v-if="isAuthenticated"
            @click.stop="$emit('chat', product)" 
            class="px-3 py-1 bg-gray-200 text-gray-700 text-sm rounded hover:bg-gray-300 transition"
          >
            Chat
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import StarRating from './StarRating.vue'

export default {
  name: 'ProductCard',
  components: {
    StarRating
  },
  props: {
    product: {
      type: Object,
      required: true
    },
    isAuthenticated: {
      type: Boolean,
      default: false
    }
  },
  emits: ['order', 'chat', 'view-details'],
  computed: {
    canRate() {
      // User can rate if they are authenticated (we'll check seller restriction in the backend)
      return this.isAuthenticated
    }
  },
  methods: {
    handleCardClick() {
      this.$emit('view-details', this.product)
    },
    
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
      event.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjNmNGY2Ii8+PGcgZmlsbD0iIzlmYTZiMiI+PHBhdGggZD0iTTE2MCA5NmMxNy42NzMgMCAzMiAxNC4zMjcgMzIgMzJzLTE0LjMyNyAzMi0zMiAzMi0zMi0xNC4zMjctMzItMzIgMTQuMzI3LTMyIDMyLTMyem0wIDEyYy0xMS4wNDYgMC0yMCA4Ljk1NC0yMCAyMHM4Ljk1NCAyMCAyMCAyMCAyMC04Ljk1NCAyMC0yMC04Ljk1NC0yMC0yMC0yMHoiLz48cGF0aCBkPSJNMTAwIDIwMGgxNjBsLTMyLTQwLTMyIDQwLTMyLTQweiIvPjwvZz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE0IiBmaWxsPSIjOWZhNmIyIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+Tm8gSW1hZ2U8L3RleHQ+PC9zdmc+'
      event.target.onerror = null
    }
  }
}
</script>
