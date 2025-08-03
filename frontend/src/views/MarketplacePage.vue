<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">PC Parts Marketplace</h1>
      <p class="text-gray-600">Buy and sell used PC components from the community</p>
    </div>
    
    <!-- Filters Section -->
    <div class="bg-white rounded-lg shadow-md p-4 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Search</label>
          <input 
            v-model="searchQuery" 
            @input="debouncedSearch"
            type="text" 
            placeholder="Search products..." 
            class="w-full px-4 py-3 border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
          >
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
          <select 
            v-model="selectedCategory" 
            @change="applyFilters"
            class="w-full px-4 py-3 border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
          >
            <option value="">All Categories</option>
            <option v-for="category in categories" :key="category" :value="category">
              {{ category }}
            </option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Condition</label>
          <select 
            v-model="selectedCondition" 
            @change="applyFilters"
            class="w-full px-4 py-3 border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
          >
            <option value="">All Conditions</option>
            <option v-for="condition in conditions" :key="condition" :value="condition">
              {{ condition }}
            </option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Sort By</label>
          <select 
            v-model="sortBy" 
            @change="applyFilters"
            class="w-full px-4 py-3 border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
          >
            <option value="name">Name</option>
            <option value="-created_at">Newest First</option>
            <option value="created_at">Oldest First</option>
            <option value="price">Price: Low to High</option>
            <option value="-price">Price: High to Low</option>
          </select>
        </div>
      </div>
      
      <!-- Price Range Filter -->
      <div class="mt-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">Price Range</label>
        <div class="flex flex-col gap-4">
          <Slider
            v-model="priceRange"
            :min="0"
            :max="100000"
            :step="1000"
            @change="applyFilters"
          />
          <div class="flex justify-between text-sm text-gray-600">
            <span>৳{{ formatPrice(priceRange[0]) }}</span>
            <span>৳{{ formatPrice(priceRange[1]) }}</span>
          </div>
        </div>
      </div>
      
      <div class="mt-4 flex justify-between items-center">
        <button 
          @click="applyFilters" 
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
        >
          Apply Filters
        </button>
        
        <button 
          v-if="isAuthenticated" 
          @click="showAddProductModal = true" 
          class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition"
        >
          Add Product
        </button>
      </div>
    </div>
    
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
    
    <!-- Products Grid - 5 products per row -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
      <ProductCard 
        v-for="product in products" 
        :key="product.id" 
        :product="product"
        @order="handleOrder"
        @chat="handleChat"
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
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Slider from '@vueform/slider'
import ProductCard from '../components/ProductCard.vue'
import AddProductModal from '../components/AddProductModal.vue'
import ChatModal from '../components/ChatModal.vue'

export default {
  name: 'MarketplacePage',
  components: {
    Slider,
    ProductCard,
    AddProductModal,
    ChatModal
  },
  setup() {
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
    const selectedProduct = ref(null)
    
    // Filters
    const searchQuery = ref('')
    const selectedCategory = ref('')
    const selectedCondition = ref('')
    const sortBy = ref('name')
    const priceRange = ref([0, 100000])
    
    // Computed
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
    
    // Methods
    const fetchProducts = async (reset = false) => {
      if (loading.value) return
      
      loading.value = true
      
      try {
        const params = new URLSearchParams()
        
        if (!reset && nextCursor.value) {
          params.append('cursor', nextCursor.value)
        }
        
        if (searchQuery.value) {
          params.append('search', searchQuery.value)
        }
        
        if (selectedCategory.value) {
          params.append('category', selectedCategory.value)
        }
        
        if (selectedCondition.value) {
          params.append('condition', selectedCondition.value)
        }
        
        if (priceRange.value[0] > 0) {
          params.append('min_price', priceRange.value[0])
        }
        
        if (priceRange.value[1] < 100000) {
          params.append('max_price', priceRange.value[1])
        }
        
        if (sortBy.value) {
          params.append('ordering', sortBy.value)
        }
        
        const {data} = await axios.get(`http://localhost:8000/api/marketplace/products/?`, {params})
        
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
    
    // Debounce timer for search
    let searchTimeout = null
    
    const handleSearch = () => {
      fetchProducts(true)
    }
    
    const debouncedSearch = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        fetchProducts(true)
      }, 500) // 500ms delay
    }
    
    const handleMinChange = () => {
      if (priceRange.value[0] > priceRange.value[1]) {
        priceRange.value[0] = priceRange.value[1]
      }
      applyFilters()
    }
    
    const handleMaxChange = () => {
      if (priceRange.value[1] < priceRange.value[0]) {
        priceRange.value[1] = priceRange.value[0]
      }
      applyFilters()
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
    
    return {
      products,
      categories,
      conditions,
      loading,
      hasMore,
      showAddProductModal,
      showChatModal,
      selectedProduct,
      searchQuery,
      selectedCategory,
      selectedCondition,
      sortBy,
      priceRange,
      isAuthenticated,
      productRows,
      handleSearch,
      debouncedSearch,
      handleMinChange,
      handleMaxChange,
      applyFilters,
      loadMore,
      handleOrder,
      handleChat,
      handleProductAdded,
      formatPrice
    }
  }
}
</script>
