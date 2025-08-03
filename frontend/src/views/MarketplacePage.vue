<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-8">
      <div class="flex justify-between items-start">
        <div>
          <h1 class="text-3xl font-bold text-gray-800 mb-2">PC Parts Marketplace</h1>
          <p class="text-gray-600">Buy and sell used PC components from the community</p>
        </div>
        <div v-if="isAuthenticated" class="flex gap-3">
          <router-link 
            to="/chats"
            class="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
            </svg>
            My Messages
          </router-link>
          <button 
            @click="showAddProductModal = true" 
            class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            Sell Product
          </button>
        </div>
      </div>
    </div>
    
    <!-- Search Bar -->
    <div class="bg-white rounded-lg shadow-md p-4 mb-6">
      <SearchWithSuggestions
        v-model="searchQuery"
        @search="handleSearch"
        @suggestion-selected="handleSuggestionSelected"
      />
      
      <!-- Search Tags -->
      <div v-if="searchTags.length > 0" class="mt-4">
        <div class="flex items-center gap-2 mb-2">
          <span class="text-sm font-medium text-gray-700">Active Filters:</span>
          <button 
            @click="clearAllSearchTags"
            class="text-xs text-red-600 hover:text-red-800 underline"
          >
            Clear All
          </button>
        </div>
        <div class="flex flex-wrap gap-2">
          <span 
            v-for="(tag, index) in searchTags" 
            :key="index"
            class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800 border border-blue-200"
          >
            {{ tag }}
            <button 
              @click="removeSearchTag(index)"
              class="ml-2 text-blue-600 hover:text-blue-800 focus:outline-none"
            >
              <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </span>
        </div>
      </div>
    </div>

    <!-- Filters Sidebar and Products -->
    <div class="flex gap-6">
      <!-- Left Sidebar Filters -->
      <div class="w-80 flex-shrink-0">
        <div class="bg-white rounded-lg shadow-md p-4 sticky top-4 max-h-screen overflow-y-auto">
          <h3 class="text-lg font-semibold text-gray-800 mb-4">Filters</h3>
          
          <!-- Category Filter -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Category</label>
            <select 
              v-model="selectedCategory" 
              @change="applyFilters"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
            >
              <option value="">All Categories</option>
              <option v-for="category in categories" :key="category" :value="category">
                {{ category }}
              </option>
            </select>
          </div>
          
          <!-- Condition Filter -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Condition</label>
            <select 
              v-model="selectedCondition" 
              @change="applyFilters"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
            >
              <option value="">All Conditions</option>
              <option v-for="condition in conditions" :key="condition" :value="condition">
                {{ condition }}
              </option>
            </select>
          </div>

          <!-- Age/Usage Duration Filter -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Age/Usage</label>
            <select 
              v-model="selectedAge" 
              @change="applyFilters"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
            >
              <option value="">Any Age</option>
              <option value="0-6months">Less than 6 months</option>
              <option value="6-12months">6-12 months</option>
              <option value="1-2years">1-2 years</option>
              <option value="2plus">2+ years</option>
            </select>
          </div>

          <!-- Distance Filter -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Distance</label>
            <select 
              v-model="selectedDistance" 
              @change="applyFilters"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
            >
              <option value="">Anywhere</option>
              <option value="5km">Within 5km</option>
              <option value="10km">Within 10km</option>
              <option value="25km">Within 25km</option>
            </select>
          </div>

          <!-- Seller Rating Filter -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Seller Rating</label>
            <select 
              v-model="selectedSellerRating" 
              @change="applyFilters"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
            >
              <option value="">Any Rating</option>
              <option value="4plus">4+ stars</option>
              <option value="3plus">3+ stars</option>
              <option value="new">New sellers</option>
            </select>
          </div>

          <!-- Warranty Status Filter -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Warranty</label>
            <select 
              v-model="selectedWarranty" 
              @change="applyFilters"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
            >
              <option value="">Any Warranty</option>
              <option value="under">Under warranty</option>
              <option value="expired">Warranty expired</option>
              <option value="none">No warranty info</option>
            </select>
          </div>

          <!-- Box/Accessories Filter -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Box & Accessories</label>
            <select 
              v-model="selectedBoxAccessories" 
              @change="applyFilters"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
            >
              <option value="">Any</option>
              <option value="box">Has original box</option>
              <option value="accessories">Has all accessories</option>
              <option value="missing">Missing items</option>
            </select>
          </div>

          <!-- Price Type Filter -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Price Type</label>
            <select 
              v-model="selectedPriceType" 
              @change="applyFilters"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
            >
              <option value="">Any</option>
              <option value="fixed">Fixed price</option>
              <option value="negotiable">Price negotiable</option>
            </select>
          </div>

          <!-- Availability Filter -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Availability</label>
            <select 
              v-model="selectedAvailability" 
              @change="applyFilters"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
            >
              <option value="">Any</option>
              <option value="now">Available now</option>
              <option value="soon">Available soon</option>
            </select>
          </div>

          <!-- Listing Age Filter -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Listed</label>
            <select 
              v-model="selectedListingAge" 
              @change="applyFilters"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
            >
              <option value="">Anytime</option>
              <option value="today">Posted today</option>
              <option value="week">This week</option>
              <option value="month">This month</option>
            </select>
          </div>

          <!-- Brand Filter -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Brand</label>
            <select 
              v-model="selectedBrand" 
              @change="applyFilters"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
            >
              <option value="">Any Brand</option>
              <option value="intel">Intel</option>
              <option value="amd">AMD</option>
              <option value="nvidia">NVIDIA</option>
              <option value="asus">ASUS</option>
              <option value="msi">MSI</option>
              <option value="corsair">Corsair</option>
              <option value="gigabyte">Gigabyte</option>
              <option value="evga">EVGA</option>
              <option value="samsung">Samsung</option>
              <option value="western-digital">Western Digital</option>
            </select>
          </div>

          <!-- Compatibility Filter -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Compatibility</label>
            <select 
              v-model="selectedCompatibility" 
              @change="applyFilters"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
            >
              <option value="">Any</option>
              <option value="lga1700">LGA1700</option>
              <option value="am4">AM4</option>
              <option value="am5">AM5</option>
              <option value="ddr4">DDR4</option>
              <option value="ddr5">DDR5</option>
              <option value="atx">ATX</option>
              <option value="micro-atx">Micro-ATX</option>
              <option value="mini-itx">Mini-ITX</option>
            </select>
          </div>

          <!-- Performance Tier Filter -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Performance Tier</label>
            <select 
              v-model="selectedPerformanceTier" 
              @change="applyFilters"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
            >
              <option value="">Any Tier</option>
              <option value="entry">Entry level</option>
              <option value="mid">Mid-range</option>
              <option value="high">High-end</option>
            </select>
          </div>
          
          <!-- Sort By Filter -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Sort By</label>
            <select 
              v-model="sortBy" 
              @change="applyFilters"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
            >
              <option value="name">Name</option>
              <option value="-created_at">Newest First</option>
              <option value="created_at">Oldest First</option>
              <option value="price">Price: Low to High</option>
              <option value="-price">Price: High to Low</option>
            </select>
          </div>
          
          <!-- Price Range Filter -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Price Range</label>
            <div class="flex flex-col gap-4">
              <Slider
                v-model="priceRange"
                :min="0"
                :max="100000"
                :step="1000"
                @change="handlePriceRangeChange"
                @update="handlePriceRangeChange"
              />
              <div class="flex justify-between text-sm text-gray-600">
                <span>৳{{ formatPrice(priceRange[0]) }}</span>
                <span>৳{{ formatPrice(priceRange[1]) }}</span>
              </div>
            </div>
          </div>
          
          <!-- Quick Actions -->
          <div v-if="isAuthenticated" class="space-y-2">
            <router-link 
              to="/chats"
              class="w-full px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition flex items-center justify-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
              </svg>
              My Messages
            </router-link>
            <button 
              @click="showAddProductModal = true" 
              class="w-full px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition flex items-center justify-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
              </svg>
              Add Product
            </button>
          </div>
        </div>
      </div>

      <!-- Products Grid -->
      <div class="flex-1">
        <!-- Loading State -->
        <div v-if="loading" class="flex justify-center items-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-700"></div>
        </div>
        
        <!-- Empty State -->
        <div v-else-if="products.length === 0" class="text-center py-12">
          <div class="text-6xl mb-4">📦</div>
          <p class="text-gray-500 text-lg mb-2">No products found matching your criteria.</p>
          <p class="text-gray-400 text-sm">Try adjusting your search or filters.</p>
        </div>
        
        <!-- Products Grid - 4 products per row -->
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          <ProductCard 
            v-for="product in products" 
            :key="product.id" 
            :product="product"
            :isAuthenticated="isAuthenticated"
            @order="handleOrder"
            @chat="handleChat"
            @view-details="handleViewDetails"
          />
        </div>
        
        <!-- Load More Button -->
        <div v-if="hasMore && !loading && products.length > 0" class="mt-8 flex justify-center">
          <button 
            @click="loadMore" 
            class="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
          >
            Load More Products
          </button>
        </div>
      </div>
    </div>

    <AddProductModal
      v-if="showAddProductModal"
      @close="showAddProductModal = false"
      @product-added="handleProductAdded"
    />

    <ChatModal
      v-if="showChatModal"
      :product="selectedProduct"
      @close="showChatModal = false"
    />

    <RatingModal
      v-if="showRatingModal"
      :show="showRatingModal"
      :product="selectedProduct"
      :existingRating="selectedProduct?.user_rating"
      @close="showRatingModal = false"
      @rating-submitted="handleRatingSubmitted"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Slider from '@vueform/slider'
import ProductCard from '../components/ProductCard.vue'
import AddProductModal from '../components/AddProductModal.vue'
import ChatModal from '../components/ChatModal.vue'
import SearchWithSuggestions from '../components/SearchWithSuggestions.vue'
import RatingModal from '../components/RatingModal.vue'

const router = useRouter()

// Reactive data
const products = ref([])
const categories = ref([])
const conditions = ref([])
const loading = ref(false)
const hasMore = ref(true)
const nextCursor = ref(null)
const showAddProductModal = ref(false)
const showChatModal = ref(false)
const showRatingModal = ref(false)
const selectedProduct = ref(null)

// Filters
const searchQuery = ref('')
const selectedCategory = ref('')
const selectedCondition = ref('')
const selectedAge = ref('')
const selectedDistance = ref('')
const selectedSellerRating = ref('')
const selectedWarranty = ref('')
const selectedBoxAccessories = ref('')
const selectedPriceType = ref('')
const selectedAvailability = ref('')
const selectedListingAge = ref('')
const selectedBrand = ref('')
const selectedCompatibility = ref('')
const selectedPerformanceTier = ref('')
const sortBy = ref('name')
const priceRange = ref([0, 100000])

const isAuthenticated = computed(() => {
  return localStorage.getItem('access_token') !== null
})

const productRows = computed(() => {
  const rows = []
  for (let i = 0; i < products.value.length; i += 5) {
    rows.push(products.value.slice(i, i + 5))
  }
  return rows
})

const fetchProducts = async (reset = false) => {
  if (loading.value) return
  
  loading.value = true
  
  try {
    const params = new URLSearchParams()
    
    if (!reset && nextCursor.value) {
      params.append('cursor', nextCursor.value)
    }
    
    // Use search tags for search instead of single query
    if (searchTags.value.length > 0) {
      params.append('search', searchTags.value.join(' '))
    }
    
    if (selectedCategory.value) {
      params.append('category', selectedCategory.value)
    }
    
    if (selectedCondition.value) {
      params.append('condition', selectedCondition.value)
    }

    if (selectedAge.value) {
      params.append('age', selectedAge.value)
    }

    if (selectedDistance.value) {
      params.append('distance', selectedDistance.value)
    }

    if (selectedSellerRating.value) {
      params.append('seller_rating', selectedSellerRating.value)
    }

    if (selectedWarranty.value) {
      params.append('warranty', selectedWarranty.value)
    }

    if (selectedBoxAccessories.value) {
      params.append('box_accessories', selectedBoxAccessories.value)
    }

    if (selectedPriceType.value) {
      params.append('price_type', selectedPriceType.value)
    }

    if (selectedAvailability.value) {
      params.append('availability', selectedAvailability.value)
    }

    if (selectedListingAge.value) {
      params.append('listing_age', selectedListingAge.value)
    }

    if (selectedBrand.value) {
      params.append('brand', selectedBrand.value)
    }

    if (selectedCompatibility.value) {
      params.append('compatibility', selectedCompatibility.value)
    }

    if (selectedPerformanceTier.value) {
      params.append('performance_tier', selectedPerformanceTier.value)
    }
    
    // Always send price range parameters
    console.log('Sending price range to API:', {
      min_price: priceRange.value[0],
      max_price: priceRange.value[1]
    })
    params.append('min_price', priceRange.value[0])
    params.append('max_price', priceRange.value[1])
    
    if (sortBy.value) {
      params.append('ordering', sortBy.value)
    }
    
    console.log('API URL with params:', `http://localhost:8000/api/marketplace/products/?${params.toString()}`)
    const {data} = await axios.get(`http://localhost:8000/api/marketplace/products/?`, {params})
    console.log('Received products:', data.results?.length, 'products')
    
    if (reset) {
      products.value = data.results
    } else {
      products.value.push(...data.results)
    }
    
    nextCursor.value = data.next ? new URL(data.next).searchParams.get('cursor') : null
    hasMore.value = !!data.next
    
  } catch (error) {
    console.error('Error fetching products:', error)
  } finally {
    loading.value = false
  }
}

const fetchCategories = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/marketplace/categories/')
    const data = await response.json()
    categories.value = data.categories
  } catch (error) {
    console.error('Error fetching categories:', error)
  }
}

const fetchConditions = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/marketplace/conditions/')
    const data = await response.json()
    conditions.value = data.conditions
  } catch (error) {
    console.error('Error fetching conditions:', error)
  }
}

// Search tags/filters
const searchTags = ref([])

const handleSearch = (query) => {
  // If query is provided, add it as a search tag
  if (query && query.trim()) {
    addSearchTag(query.trim())
    searchQuery.value = '' // Clear the search input
  }
  fetchProducts(true)
}

const handleSuggestionSelected = (suggestion) => {
  // Add the selected suggestion as a search tag
  addSearchTag(suggestion.text)
  searchQuery.value = '' // Clear the search input
  fetchProducts(true)
}

const addSearchTag = (tag) => {
  // Avoid duplicate tags
  if (!searchTags.value.includes(tag)) {
    searchTags.value.push(tag)
  }
}

const removeSearchTag = (index) => {
  searchTags.value.splice(index, 1)
  fetchProducts(true)
}

const clearAllSearchTags = () => {
  searchTags.value = []
  searchQuery.value = ''
  fetchProducts(true)
}

// Debounce function to prevent too many API calls
let priceRangeTimeout = null

const handlePriceRangeChange = () => {
  console.log('Price range changed:', priceRange.value)
  console.log('Min price:', priceRange.value[0], 'Max price:', priceRange.value[1])
  
  // Clear existing timeout
  if (priceRangeTimeout) {
    clearTimeout(priceRangeTimeout)
  }
  
  // Set new timeout to debounce the API call
  priceRangeTimeout = setTimeout(() => {
    applyFilters()
  }, 500) // Wait 500ms after user stops dragging
}

const applyFilters = () => {
  fetchProducts(true)
}

const loadMore = () => {
  fetchProducts(false)
}

const handleOrder = (product) => {
  if (!isAuthenticated.value) {
    router.push('/login')
    return
  }
  // Handle order logic
  console.log('Order product:', product)
}

const handleChat = (product) => {
  if (!isAuthenticated.value) {
    router.push('/login')
    return
  }
  console.log('Opening chat for product:', product)
  selectedProduct.value = product
  showChatModal.value = true
  console.log('Chat modal should be visible:', showChatModal.value)
}

const handleRate = (product) => {
  if (!isAuthenticated.value) {
    router.push('/login')
    return
  }
  selectedProduct.value = product
  showRatingModal.value = true
}

const handleViewDetails = (product) => {
  router.push(`/marketplace/product/${product.id}`)
}

const handleRatingSubmitted = () => {
  showRatingModal.value = false
  // Refresh products to get updated ratings
  fetchProducts(true)
}

const handleProductAdded = () => {
  showAddProductModal.value = false
  fetchProducts(true)
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-BD').format(price)
}

// Lifecycle
onMounted(() => {
  fetchProducts(true)
  fetchCategories()
  fetchConditions()
})
</script>
