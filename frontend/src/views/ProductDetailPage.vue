<template>
  <div class="container mx-auto px-4 py-8">
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-700"></div>
    </div>

    <div v-else-if="error" class="text-center py-12">
      <div class="text-6xl mb-4">❌</div>
      <p class="text-gray-500 text-lg mb-2">{{ error }}</p>
      <button 
        @click="$router.go(-1)" 
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
      >
        Go Back
      </button>
    </div>

    <div v-else-if="product" class="max-w-6xl mx-auto">
      <nav class="mb-6">
        <ol class="flex items-center space-x-2 text-sm text-gray-500">
          <li><router-link to="/marketplace" class="hover:text-blue-600">Marketplace</router-link></li>
          <li><span class="mx-2">/</span></li>
          <li><span class="text-gray-400">{{ product.category }}</span></li>
          <li><span class="mx-2">/</span></li>
          <li><span class="text-gray-900 font-medium">{{ product.name }}</span></li>
        </ol>
      </nav>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div class="bg-white rounded-lg shadow-md p-6">
          <img 
            :src="product.image || '/placeholder-product.jpg'" 
            :alt="product.name"
            @error="handleImageError"
            class="w-full h-96 object-contain bg-gray-100 rounded-lg"
          />
        </div>

        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="mb-4">
            <span class="inline-block px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full mb-2">
              {{ product.category }}
            </span>
            <span class="inline-block px-3 py-1 bg-green-100 text-green-800 text-sm font-medium rounded-full mb-2 ml-2">
              {{ product.condition }}
            </span>
          </div>

          <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ product.name }}</h1>

          <div class="mb-6">
            <div class="flex items-center space-x-4">
              <span class="text-4xl font-bold text-blue-700">৳{{ formatPrice(product.price) }}</span>
              <span v-if="product.price_type === 'negotiable'" class="text-sm text-gray-500 bg-yellow-100 px-2 py-1 rounded">
                Negotiable
              </span>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4 mb-6 text-sm">
            <div v-if="product.brand">
              <span class="font-medium text-gray-700">Brand:</span>
              <span class="ml-2 text-gray-600">{{ product.brand }}</span>
            </div>
            <div v-if="product.age">
              <span class="font-medium text-gray-700">Age:</span>
              <span class="ml-2 text-gray-600">{{ product.age }}</span>
            </div>
            <div v-if="product.warranty">
              <span class="font-medium text-gray-700">Warranty:</span>
              <span class="ml-2 text-gray-600">{{ product.warranty }}</span>
            </div>
            <div v-if="product.box_accessories">
              <span class="font-medium text-gray-700">Box & Accessories:</span>
              <span class="ml-2 text-gray-600">{{ product.box_accessories }}</span>
            </div>
            <div v-if="product.availability">
              <span class="font-medium text-gray-700">Availability:</span>
              <span class="ml-2 text-gray-600">{{ product.availability }}</span>
            </div>
            <div v-if="product.compatibility">
              <span class="font-medium text-gray-700">Compatibility:</span>
              <span class="ml-2 text-gray-600">{{ product.compatibility }}</span>
            </div>
          </div>

          <div class="mb-6 p-4 bg-gray-50 rounded-lg">
            <h3 class="font-medium text-gray-900 mb-2">Seller Information</h3>
            <div class="flex items-center space-x-4">
              <div class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold">
                {{ getSellerInitial(product.seller_name) }}
              </div>
              <div class="flex-1">
                <p class="font-medium text-gray-900">{{ product.seller_name || 'Demo Seller' }}</p>
                <p class="text-sm text-gray-500">Member since {{ formatDate(product.created_at) }}</p>
                <div class="mt-2">
                  <StarRating 
                    :modelValue="product.seller_rating || 0"
                    :count="product.seller_rating_count || 0"
                    :interactive="false"
                    :showText="true"
                  />
                </div>
              </div>
              <div class="text-right">
                <button 
                  v-if="canRateSeller"
                  @click="showRatingModal = true" 
                  class="px-3 py-1 bg-yellow-500 text-white text-sm rounded hover:bg-yellow-600 transition"
                >
                  {{ userSellerRating ? 'Update' : 'Rate Seller' }}
                </button>
              </div>
            </div>
          </div>

          <div class="flex space-x-4">
            <button 
              @click="handleAddToCart" 
              :disabled="!product.is_available"
              class="flex-1 px-6 py-3 text-lg font-medium rounded-lg transition"
              :class="product.is_available !== false
                ? 'bg-green-600 text-white hover:bg-green-700' 
                : 'bg-gray-400 text-white cursor-not-allowed'"
            >
              {{ product.is_available !== false ? 'Add to Cart' : 'Sold Out' }}
            </button>
            <button 
              @click="handleChat" 
              class="px-6 py-3 bg-gray-200 text-gray-700 text-lg font-medium rounded-lg hover:bg-gray-300 transition"
            >
              Chat with Seller
            </button>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">Description</h2>
        <p class="text-gray-700 leading-relaxed whitespace-pre-line">{{ product.description }}</p>
      </div>

    </div>

    <!-- Rating Modal -->
    <RatingModal
      v-if="showRatingModal"
      :show="showRatingModal"
      :product="product"
      :existingRating="userSellerRating"
      @close="showRatingModal = false"
      @rating-submitted="handleRatingSubmitted"
    />

    <!-- Chat Modal -->
    <ChatModal
      v-if="showChatModal"
      :product="product"
      @close="showChatModal = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import StarRating from '../components/StarRating.vue'
import RatingModal from '../components/RatingModal.vue'
import ChatModal from '../components/ChatModal.vue'

const route = useRoute()
const router = useRouter()

const product = ref(null)
const userSellerRating = ref(null)
const loading = ref(true)
const error = ref('')
const showRatingModal = ref(false)
const showChatModal = ref(false)

const isAuthenticated = computed(() => {
  return localStorage.getItem('access_token') !== null
})

const canRateSeller = computed(() => {
  if (!isAuthenticated.value || !product.value) {
    return false
  }
  return product.value.seller !== getCurrentUserId()
})

const getCurrentUserId = () => {
  try {
    const token = localStorage.getItem('access_token')
    if (!token) return null
    
    // Decode JWT token to get user ID
    const payload = JSON.parse(atob(token.split('.')[1]))
    console.log('JWT payload:', payload)
    return payload.user_id || payload.id
  } catch (error) {
    console.error('Error decoding token:', error)
    return null
  }
}

const fetchProduct = async () => {
  try {
    loading.value = true
    error.value = ''
    const productId = route.params.id
    
    const headers = {}
    const token = localStorage.getItem('access_token')
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    
    const response = await axios.get(
      `http://localhost:8000/api/marketplace/products/${productId}/`,
      { headers }
    )
    
    if (response.data) {
      product.value = response.data
      userSellerRating.value = response.data.user_seller_rating || null
    } else {
      error.value = 'Product not found'
    }
    
  } catch (err) {
    if (err.response?.status === 404) {
      error.value = 'Product not found'
    } else {
      error.value = 'Failed to load product details'
    }
  } finally {
    loading.value = false
  }
}

const handleRatingSubmitted = () => {
  showRatingModal.value = false
  fetchProduct()
}

const handleAddToCart = () => {
  if (!isAuthenticated.value) {
    router.push('/login')
    return
  }
  // Add to cart functionality would be implemented here
  alert('Product added to cart!')
}

const handleChat = () => {
  if (!isAuthenticated.value) {
    router.push('/login')
    return
  }
  showChatModal.value = true
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-BD').format(price)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getSellerInitial = (sellerName) => {
  if (!sellerName) return 'D'
  return sellerName.charAt(0).toUpperCase()
}

const handleImageError = (event) => {
  event.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjNmNGY2Ii8+PGcgZmlsbD0iIzlmYTZiMiI+PHBhdGggZD0iTTE2MCA5NmMxNy42NzMgMCAzMiAxNC4zMjcgMzIgMzJzLTE0LjMyNyAzMi0zMiAzMi0zMi0xNC4zMjctMzItMzIgMTQuMzI3LTMyIDMyLTMyem0wIDEyYy0xMS4wNDYgMC0yMCA4Ljk1NC0yMCAyMHM4Ljk1NCAyMCAyMCAyMCAyMC04Ljk1NCAyMC0yMC04Ljk1NC0yMC0yMC0yMHoiLz48cGF0aCBkPSJNMTAwIDIwMGgxNjBsLTMyLTQwLTMyIDQwLTMyLTQweiIvPjwvZz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE0IiBmaWxsPSIjOWZhNmIyIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+Tm8gSW1hZ2U8L3RleHQ+PC9zdmc+'
  event.target.onerror = null
}

onMounted(() => {
  fetchProduct()
})
</script>
