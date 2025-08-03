<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold text-gray-900">Rate Product</h3>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
      
      <!-- Product Info -->
      <div class="mb-4 p-3 bg-gray-50 rounded-lg">
        <h4 class="font-medium text-gray-900">{{ product.name }}</h4>
        <p class="text-sm text-gray-600">{{ product.category }} • ৳{{ formatPrice(product.price) }}</p>
      </div>
      
      <!-- Rating Section -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">Your Rating</label>
        <StarRating 
          v-model="rating"
          :interactive="true"
          :showText="false"
        />
        <p class="text-sm text-gray-500 mt-1">Click on stars to rate</p>
      </div>
      
      <!-- Review Section -->
      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-700 mb-2">Review (Optional)</label>
        <textarea
          v-model="review"
          rows="4"
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
          placeholder="Share your experience with this product..."
        ></textarea>
      </div>
      
      <!-- Action Buttons -->
      <div class="flex justify-end space-x-3">
        <button
          @click="$emit('close')"
          class="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 transition"
        >
          Cancel
        </button>
        <button
          @click="submitRating"
          :disabled="rating === 0 || submitting"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
        >
          {{ submitting ? 'Submitting...' : (existingRating ? 'Update Rating' : 'Submit Rating') }}
        </button>
      </div>
      
      <!-- Error Message -->
      <div v-if="error" class="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'
import StarRating from './StarRating.vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  product: {
    type: Object,
    required: true
  },
  existingRating: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'rating-submitted'])

const rating = ref(0)
const review = ref('')
const submitting = ref(false)
const error = ref('')

// Watch for existing rating to populate form
watch(() => props.existingRating, (newRating) => {
  if (newRating) {
    rating.value = newRating.rating
    review.value = newRating.review || ''
  } else {
    rating.value = 0
    review.value = ''
  }
}, { immediate: true })

// Reset form when modal is closed
watch(() => props.show, (newShow) => {
  if (!newShow) {
    error.value = ''
  }
})

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-BD').format(price)
}

const submitRating = async () => {
  if (rating.value === 0) {
    error.value = 'Please select a rating'
    return
  }
  
  submitting.value = true
  error.value = ''
  
  try {
    const token = localStorage.getItem('access_token')
    const data = {
      rating: rating.value,
      review: review.value.trim() || null
    }
    
    await axios.post(
      `http://localhost:8000/api/marketplace/products/${props.product.id}/ratings/create/`,
      data,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    )
    
    emit('rating-submitted')
    emit('close')
  } catch (err) {
    console.error('Error submitting rating:', err)
    error.value = err.response?.data?.error || 'Failed to submit rating. Please try again.'
  } finally {
    submitting.value = false
  }
}
</script>
