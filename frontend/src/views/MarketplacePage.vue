<template>
  <div class="p-5 max-w-7xl mx-auto">
    <div class="text-center mb-8">
      <h1 class="text-gray-800 mb-5 text-3xl font-bold">PC Parts Marketplace</h1>
      <div class="flex justify-center gap-2.5 mb-5">
        <input
          v-model="searchQuery"
          @input="handleSearch"
          type="text"
          placeholder="Search for products..."
          class="px-3 py-3 border-2 border-gray-300 rounded-lg w-96 text-base focus:outline-none focus:border-blue-500"
        />
        <button @click="handleSearch" class="px-6 py-3 bg-blue-500 text-white border-none rounded-lg cursor-pointer text-base hover:bg-blue-600 transition-colors">
          Search
        </button>
      </div>
    </div>

    <div class="flex gap-8 lg:flex-row flex-col">
      <!-- Sidebar Filters -->
      <div class="w-full lg:w-64 bg-gray-50 p-5 rounded-lg h-fit">
        <div class="mb-6">
          <h3 class="mb-2.5 text-gray-800 text-base font-semibold">Category</h3>
          <select v-model="selectedCategory" @change="applyFilters" class="w-full p-2 border border-gray-300 rounded text-sm focus:outline-none focus:border-blue-500">
            <option value="">All Categories</option>
            <option v-for="category in categories" :key="category" :value="category">
              {{ category }}
            </option>
          </select>
        </div>

        <div class="mb-6">
          <h3 class="mb-2.5 text-gray-800 text-base font-semibold">Condition</h3>
          <select v-model="selectedCondition" @change="applyFilters" class="w-full p-2 border border-gray-300 rounded text-sm focus:outline-none focus:border-blue-500">
            <option value="">All Conditions</option>
            <option v-for="condition in conditions" :key="condition" :value="condition">
              {{ condition }}
            </option>
          </select>
        </div>

        <div class="mb-6">
          <h3 class="mb-2.5 text-gray-800 text-base font-semibold">Price Range</h3>
          <div class="flex flex-col gap-2.5">
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

        <div v-if="isAuthenticated" class="mb-6">
          <button @click="showAddProductModal = true" class="w-full px-3 py-3 bg-green-500 text-white border-none rounded-lg cursor-pointer text-base hover:bg-green-600 transition-colors">
            Add Product
          </button>
        </div>
      </div>

      <!-- Product Grid -->
      <div class="flex-1">
        <div>
          <div
            v-for="(productRow, index) in productRows"
            :key="index"
            class="flex gap-5 mb-5 flex-wrap"
          >
            <ProductCard
              v-for="product in productRow"
              :key="product.id"
              :product="product"
              @order="handleOrder"
              @chat="handleChat"
            />
          </div>
        </div>

        <!-- No products message -->
        <div v-if="!loading && products.length === 0" class="text-center py-16 px-5 text-gray-600">
          <div class="text-6xl mb-5">📦</div>
          <h3 class="text-2xl text-gray-800 mb-2.5 font-semibold">No products found</h3>
          <p class="text-base mb-8 max-w-md mx-auto">Try adjusting your search criteria or filters to find what you're looking for.</p>
        </div>

        <!-- Loading indicator -->
        <div v-if="loading" class="text-center py-5 text-gray-600">Loading more products...</div>

        <!-- Load more button -->
        <div v-if="hasMore && !loading && products.length > 0" class="text-center mt-8">
          <button @click="loadMore" class="px-6 py-3 bg-blue-500 text-white border-none rounded-lg cursor-pointer text-base hover:bg-blue-600 transition-colors">
            Load More
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
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
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
        
        const response = await fetch(`http://localhost:8000/api/marketplace/products/?${params}`)
        const data = await response.json()
        
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
    
    const handleSearch = () => {
      fetchProducts(true)
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
      priceRange,
      isAuthenticated,
      productRows,
      handleSearch,
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

<style scoped>
@import '@vueform/slider/themes/default.css';
</style>
