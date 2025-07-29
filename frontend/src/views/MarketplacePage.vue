<template>
  <div class="marketplace">
    <div class="marketplace-header">
      <h1>PC Parts Marketplace</h1>
      <div class="search-bar">
        <input
          v-model="searchQuery"
          @input="handleSearch"
          type="text"
          placeholder="Search for products..."
          class="search-input"
        />
        <button @click="handleSearch" class="search-btn">Search</button>
      </div>
    </div>

    <div class="marketplace-content">
      <!-- Sidebar Filters -->
      <div class="sidebar">
        <div class="filter-section">
          <h3>Category</h3>
          <select v-model="selectedCategory" @change="applyFilters">
            <option value="">All Categories</option>
            <option v-for="category in categories" :key="category" :value="category">
              {{ category }}
            </option>
          </select>
        </div>

        <div class="filter-section">
          <h3>Condition</h3>
          <select v-model="selectedCondition" @change="applyFilters">
            <option value="">All Conditions</option>
            <option v-for="condition in conditions" :key="condition" :value="condition">
              {{ condition }}
            </option>
          </select>
        </div>

        <div class="filter-section">
          <h3>Price Range</h3>
          <div class="price-slider">
            <input
              type="range"
              v-model="priceRange.min"
              :min="0"
              :max="100000"
              @input="applyFilters"
              class="slider"
            />
            <input
              type="range"
              v-model="priceRange.max"
              :min="0"
              :max="100000"
              @input="applyFilters"
              class="slider"
            />
            <div class="price-labels">
              <span>৳{{ priceRange.min }}</span>
              <span>৳{{ priceRange.max }}</span>
            </div>
          </div>
        </div>

        <div class="filter-section" v-if="isAuthenticated">
          <button @click="showAddProductModal = true" class="add-product-btn">
            Add Product
          </button>
        </div>
      </div>

      <!-- Product Grid -->
      <div class="product-grid">
        <div class="products-container">
          <div
            v-for="(productRow, index) in productRows"
            :key="index"
            class="product-row"
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

        <!-- Loading indicator -->
        <div v-if="loading" class="loading">Loading more products...</div>

        <!-- Load more button -->
        <div v-if="hasMore && !loading" class="load-more">
          <button @click="loadMore" class="load-more-btn">Load More</button>
        </div>
      </div>
    </div>

    <!-- Add Product Modal -->
    <AddProductModal
      v-if="showAddProductModal"
      @close="showAddProductModal = false"
      @product-added="handleProductAdded"
    />

    <!-- Chat Modal -->
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
import ProductCard from '../components/ProductCard.vue'
import AddProductModal from '../components/AddProductModal.vue'
import ChatModal from '../components/ChatModal.vue'

export default {
  name: 'MarketplacePage',
  components: {
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
    const priceRange = reactive({
      min: 0,
      max: 100000
    })
    
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
        
        if (priceRange.min > 0) {
          params.append('min_price', priceRange.min)
        }
        
        if (priceRange.max < 100000) {
          params.append('max_price', priceRange.max)
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
        alert('Please log in to order products')
        return
      }
      // Handle order logic
      console.log('Order product:', product)
    }
    
    const handleChat = (product) => {
      if (!isAuthenticated.value) {
        alert('Please log in to chat with sellers')
        return
      }
      selectedProduct.value = product
      showChatModal.value = true
    }
    
    const handleProductAdded = () => {
      showAddProductModal.value = false
      fetchProducts(true)
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
      handleProductAdded
    }
  }
}
</script>

<style scoped>
.marketplace {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.marketplace-header {
  text-align: center;
  margin-bottom: 30px;
}

.marketplace-header h1 {
  color: #333;
  margin-bottom: 20px;
}

.search-bar {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

.search-input {
  padding: 12px;
  border: 2px solid #ddd;
  border-radius: 8px;
  width: 400px;
  font-size: 16px;
}

.search-btn {
  padding: 12px 24px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
}

.search-btn:hover {
  background: #0056b3;
}

.marketplace-content {
  display: flex;
  gap: 30px;
}

.sidebar {
  width: 250px;
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  height: fit-content;
}

.filter-section {
  margin-bottom: 25px;
}

.filter-section h3 {
  margin-bottom: 10px;
  color: #333;
  font-size: 16px;
}

.filter-section select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.price-slider {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.slider {
  width: 100%;
}

.price-labels {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #666;
}

.add-product-btn {
  width: 100%;
  padding: 12px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
}

.add-product-btn:hover {
  background: #218838;
}

.product-grid {
  flex: 1;
}

.product-row {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #666;
}

.load-more {
  text-align: center;
  margin-top: 30px;
}

.load-more-btn {
  padding: 12px 24px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
}

.load-more-btn:hover {
  background: #0056b3;
}

@media (max-width: 768px) {
  .marketplace-content {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
  }
  
  .search-input {
    width: 100%;
    max-width: 300px;
  }
  
  .product-row {
    justify-content: center;
  }
}
</style>
