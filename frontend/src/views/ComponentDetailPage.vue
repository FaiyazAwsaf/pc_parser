<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      <p class="ml-2 text-gray-600">Loading component details...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-8">
      <p class="text-red-600">{{ error }}</p>
      <button @click="fetchData" class="mt-2 bg-blue-600 text-white px-4 py-2 rounded">Retry</button>
    </div>

    <!-- Component Details -->
    <div v-else-if="component" class="max-w-6xl mx-auto px-4 py-8">

      <!-- Component Header -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <div class="flex flex-col md:flex-row gap-6">
          <div class="md:w-1/3">
            <img 
              :src="component.image || '/placeholder-component.png'" 
              :alt="component.name"
              class="w-full h-64 object-contain bg-gray-100 rounded-lg"
            />
          </div>
          <div class="md:w-2/3">
            <div class="mb-2">
              <span class="inline-block bg-blue-100 text-blue-800 text-sm px-3 py-1 rounded-full">
                {{ component.category.name }}
              </span>
            </div>
            <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ component.name }}</h1>
            <p class="text-lg text-gray-600 mb-4">{{ component.brand }} {{ component.model }}</p>
            
            <!-- Price Information -->
            <div v-if="offers && offers.length > 0" class="mb-4">
              <h3 class="text-lg font-semibold mb-2">Available from:</h3>
              <div class="space-y-2">
                <div v-for="offer in offers.slice(0, 3)" :key="offer.id" class="flex justify-between items-center border rounded-lg p-3">
                  <div>
                    <p class="font-medium">{{ offer.retailer_name }}</p>
                    <p class="text-sm text-gray-500">{{ offer.retailer }}</p>
                  </div>
                  <div class="text-right">
                    <p class="text-lg font-bold text-green-600">Tk. {{ offer.price }}</p>
                    <a 
                      :href="offer.url" 
                      target="_blank" 
                      class="text-sm bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
                    >
                      View Deal
                    </a>
                  </div>
                </div>
              </div>
              <button 
                v-if="offers.length > 3" 
                @click="showAllOffers = !showAllOffers"
                class="mt-2 text-blue-600 hover:text-blue-800"
              >
                {{ showAllOffers ? 'Show Less' : `Show ${offers.length - 3} More Offers` }}
              </button>
            </div>
            <div v-else class="mb-4">
              <p class="text-gray-500">No pricing information available</p>
            </div>
          </div>
        </div>
      </div>

      <!-- All Offers (when expanded) -->
      <div v-if="showAllOffers && offers && offers.length > 3" class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h3 class="text-xl font-bold mb-4">All Available Offers</h3>
        <div class="grid gap-3">
          <div v-for="offer in offers.slice(3)" :key="offer.id" class="flex justify-between items-center border rounded-lg p-3">
            <div>
              <p class="font-medium">{{ offer.retailer_name }}</p>
              <p class="text-sm text-gray-500">{{ offer.retailer }}</p>
              <p class="text-xs" :class="offer.availability ? 'text-green-600' : 'text-red-600'">
                {{ offer.availability ? 'In Stock' : 'Out of Stock' }}
              </p>
            </div>
            <div class="text-right">
              <p class="text-lg font-bold text-green-600">Tk.{{ offer.price }}</p>
              <a 
                :href="offer.url" 
                target="_blank" 
                class="text-sm bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
              >
                View Deal
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Specifications -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h3 class="text-xl font-bold mb-4">Specifications</h3>
        <div v-if="component.specs && Object.keys(component.specs).length > 0" class="grid md:grid-cols-2 gap-4">
          <div v-for="(value, key) in component.specs" :key="key" class="border-b pb-2">
            <div class="flex justify-between">
              <span class="font-medium text-gray-700 capitalize">{{ formatSpecKey(key) }}:</span>
              <span class="text-gray-900">{{ value || 'N/A' }}</span>
            </div>
          </div>
        </div>
        <div v-else class="text-gray-500">
          No detailed specifications available.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// Data
const component = ref(null)
const offers = ref([])
const loading = ref(true)
const error = ref(null)
const showAllOffers = ref(false)

// Get component ID from route params
const componentId = route.params.slug || route.params.id

// Format spec keys for display
const formatSpecKey = (key) => {
  return key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

// Fetch component data
const fetchData = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await fetch(`http://localhost:8000/api/components/${componentId}/offers/`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    component.value = data.component
    offers.value = data.offers.sort((a, b) => (a.price || 999999) - (b.price || 999999))
    
  } catch (err) {
    error.value = `Failed to load component: ${err.message}`
    console.error('Error fetching component:', err)
  } finally {
    loading.value = false
  }
}

// Fetch data on component mount
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>