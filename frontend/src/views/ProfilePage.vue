<template>
  <div class="container mx-auto px-4 py-8">
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-700"></div>
    </div>

    <div v-else class="max-w-6xl mx-auto">
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <div class="flex items-center space-x-6">
          <div class="w-24 h-24 bg-blue-500 rounded-full flex items-center justify-center text-white text-3xl font-bold">
            {{ userInitials }}
          </div>
          <div class="flex-1">
            <h1 class="text-3xl font-bold text-gray-800">{{ user.first_name }} {{ user.last_name }}</h1>
            <p class="text-gray-600">{{ user.email }}</p>
            <p class="text-sm text-gray-500 mt-1">Member since {{ formatDate(user.date_joined) }}</p>
            <div class="flex items-center mt-2 space-x-3">
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                ✓ Verified Email
              </span>
              <div class="flex items-center space-x-1">
                <div class="flex items-center">
                  <svg v-for="i in 5" :key="i" class="w-4 h-4" :class="i <= Math.floor(user.seller_rating || 0) ? 'text-yellow-400' : 'text-gray-300'" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                  </svg>
                </div>
                <span class="text-sm text-gray-600">{{ user.seller_rating || 0 }}/5 ({{ user.seller_rating_count || 0 }} reviews)</span>
              </div>
            </div>
          </div>
          <button 
            @click="showEditModal = true"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
          >
            Edit Profile
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-blue-100 text-blue-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Products Listed</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.totalProducts }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-green-100 text-green-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Items Sold</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.totalSold }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-yellow-100 text-yellow-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Total Revenue</p>
              <p class="text-2xl font-semibold text-gray-900">৳{{ formatPrice(stats.totalRevenue) }}</p>
            </div>
          </div>
        </div>

        <div 
          @click="$router.push('/chats')"
          class="bg-white rounded-lg shadow-md p-6 cursor-pointer hover:shadow-lg transition-shadow"
        >
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-purple-100 text-purple-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
              </svg>
            </div>
            <div class="ml-4 flex-1">
              <p class="text-sm font-medium text-gray-600">Active Chats</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.activeChats }}</p>
            </div>
            <div class="ml-2">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-md">
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8 px-6">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                'py-4 px-1 border-b-2 font-medium text-sm',
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              {{ tab.name }}
            </button>
          </nav>
        </div>

        <div class="p-6">
          <div v-if="activeTab === 'products'">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg font-medium text-gray-900">My Products</h3>
              <button 
                @click="showAddProductModal = true"
                class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition"
              >
                Add Product
              </button>
            </div>
            
            <div v-if="myProducts.length === 0" class="text-center py-8">
              <div class="text-4xl mb-4">📦</div>
              <p class="text-gray-500">You haven't listed any products yet.</p>
            </div>
            
            <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div 
                v-for="product in myProducts" 
                :key="product.id"
                class="border rounded-lg p-4 hover:shadow-md transition"
              >
                <img 
                  :src="product.image || 'https://via.placeholder.com/200x150'" 
                  :alt="product.name"
                  class="w-full h-32 object-cover rounded mb-3"
                />
                <h4 class="font-medium text-gray-900 mb-1">{{ product.name }}</h4>
                <p class="text-sm text-gray-600 mb-2">{{ product.category }} - {{ product.condition }}</p>
                <p class="text-lg font-semibold text-blue-600 mb-3">৳{{ formatPrice(product.price) }}</p>
                <div class="flex space-x-2">
                  <button 
                    @click="editProduct(product)"
                    class="flex-1 px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
                  >
                    Edit
                  </button>
                  <button 
                    @click="deleteProduct(product)"
                    class="flex-1 px-3 py-1 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div v-if="activeTab === 'sales'">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Sales History</h3>
            
            <div v-if="salesHistory.length === 0" class="text-center py-8">
              <div class="text-4xl mb-4">💰</div>
              <p class="text-gray-500">No sales yet. Keep promoting your products!</p>
            </div>
            
            <div v-else class="space-y-4">
              <div 
                v-for="sale in salesHistory" 
                :key="sale.id"
                class="border rounded-lg p-4 flex items-center justify-between"
              >
                <div class="flex items-center space-x-4">
                  <img 
                    :src="sale.product_image || 'https://via.placeholder.com/60x60'" 
                    :alt="sale.product_name"
                    class="w-12 h-12 object-cover rounded"
                  />
                  <div>
                    <h4 class="font-medium text-gray-900">{{ sale.product_name }}</h4>
                    <p class="text-sm text-gray-600">Sold to {{ sale.buyer_name }}</p>
                    <p class="text-xs text-gray-500">{{ formatDate(sale.created_at) }}</p>
                  </div>
                </div>
                <div class="text-right">
                  <p class="text-lg font-semibold text-green-600">৳{{ formatPrice(sale.total_price) }}</p>
                  <span :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                    sale.status === 'completed' ? 'bg-green-100 text-green-800' : 
                    sale.status === 'pending' ? 'bg-yellow-100 text-yellow-800' : 
                    'bg-gray-100 text-gray-800'
                  ]">
                    {{ sale.status }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div v-if="activeTab === 'purchases'">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Purchase History</h3>
            
            <div v-if="purchaseHistory.length === 0" class="text-center py-8">
              <div class="text-4xl mb-4">🛒</div>
              <p class="text-gray-500">No purchases yet. Browse the marketplace!</p>
            </div>
            
            <div v-else class="space-y-4">
              <div 
                v-for="purchase in purchaseHistory" 
                :key="purchase.id"
                class="border rounded-lg p-4 flex items-center justify-between"
              >
                <div class="flex items-center space-x-4">
                  <img 
                    :src="purchase.product_image || 'https://via.placeholder.com/60x60'" 
                    :alt="purchase.product_name"
                    class="w-12 h-12 object-cover rounded"
                  />
                  <div>
                    <h4 class="font-medium text-gray-900">{{ purchase.product_name }}</h4>
                    <p class="text-sm text-gray-600">From {{ purchase.seller_name }}</p>
                    <p class="text-xs text-gray-500">{{ formatDate(purchase.created_at) }}</p>
                  </div>
                </div>
                <div class="text-right">
                  <p class="text-lg font-semibold text-blue-600">৳{{ formatPrice(purchase.total_price) }}</p>
                  <span :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                    purchase.status === 'completed' ? 'bg-green-100 text-green-800' : 
                    purchase.status === 'pending' ? 'bg-yellow-100 text-yellow-800' : 
                    'bg-gray-100 text-gray-800'
                  ]">
                    {{ purchase.status }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div v-if="activeTab === 'analytics'">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Sales Analytics</h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="bg-gray-50 rounded-lg p-4">
                <h4 class="font-medium text-gray-900 mb-3">Sales by Category</h4>
                <div class="space-y-2">
                  <div v-for="category in categoryStats" :key="category.name" class="flex justify-between items-center">
                    <span class="text-sm text-gray-600">{{ category.name }}</span>
                    <div class="flex items-center space-x-2">
                      <div class="w-20 bg-gray-200 rounded-full h-2">
                        <div 
                          class="bg-blue-600 h-2 rounded-full" 
                          :style="{ width: category.percentage + '%' }"
                        ></div>
                      </div>
                      <span class="text-sm font-medium">{{ category.count }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="bg-gray-50 rounded-lg p-4">
                <h4 class="font-medium text-gray-900 mb-3">Monthly Revenue</h4>
                <div class="space-y-2">
                  <div v-for="month in monthlyRevenue" :key="month.month" class="flex justify-between">
                    <span class="text-sm text-gray-600">{{ month.month }}</span>
                    <span class="text-sm font-medium">৳{{ formatPrice(month.revenue) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Edit Profile</h3>
        <form @submit.prevent="updateProfile">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">First Name</label>
              <input 
                v-model="editForm.first_name"
                type="text" 
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
              <input 
                v-model="editForm.last_name"
                type="text" 
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          <div class="flex justify-end space-x-3 mt-6">
            <button 
              type="button"
              @click="showEditModal = false"
              class="px-4 py-2 text-gray-700 border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Cancel
            </button>
            <button 
              type="submit"
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Save Changes
            </button>
          </div>
        </form>
      </div>
    </div>

    <AddProductModal
      v-if="showAddProductModal"
      @close="showAddProductModal = false"
      @product-added="handleProductAdded"
    />

    <EditProductModal
      v-if="showEditProductModal && selectedProduct"
      :product="selectedProduct"
      @close="showEditProductModal = false"
      @product-updated="handleProductUpdated"
    />

    <div v-if="showDeleteModal" class="fixed inset-0 flex items-center justify-center z-50" style="background-color: rgba(0, 0, 0, 0.4);">
      <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <div class="flex items-center mb-4">
          <div class="flex-shrink-0 w-10 h-10 mx-auto bg-red-100 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
            </svg>
          </div>
        </div>
        <div class="text-center">
          <h3 class="text-lg font-medium text-gray-900 mb-2">Delete Product</h3>
          <p class="text-sm text-gray-500 mb-6">
            Are you sure you want to delete "{{ productToDelete?.name }}"? This action cannot be undone.
          </p>
          <div class="flex space-x-3">
            <button 
              @click="showDeleteModal = false"
              class="flex-1 px-4 py-2 text-gray-700 border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500"
            >
              Cancel
            </button>
            <button 
              @click="confirmDelete"
              class="flex-1 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import AddProductModal from '../components/AddProductModal.vue'
import EditProductModal from '../components/EditProductModal.vue'

const router = useRouter()
const loading = ref(true)
const showEditModal = ref(false)
const showAddProductModal = ref(false)
const showEditProductModal = ref(false)
const selectedProduct = ref(null)
const showDeleteModal = ref(false)
const productToDelete = ref(null)
const activeTab = ref('products')

const user = ref({})
const myProducts = ref([])
const salesHistory = ref([])
const purchaseHistory = ref([])
const stats = ref({
  totalProducts: 0,
  totalSold: 0,
  totalRevenue: 0,
  activeChats: 0
})

const editForm = reactive({
  first_name: '',
  last_name: ''
})

const tabs = [
  { id: 'products', name: 'My Products' },
  { id: 'sales', name: 'Sales History' },
  { id: 'purchases', name: 'Purchase History' },
  { id: 'analytics', name: 'Analytics' }
]

const userInitials = computed(() => {
  if (user.value.first_name && user.value.last_name) {
    return user.value.first_name.charAt(0) + user.value.last_name.charAt(0)
  }
  return user.value.username ? user.value.username.charAt(0).toUpperCase() : 'U'
})

const categoryStats = computed(() => {
  const categories = {}
  myProducts.value.forEach(product => {
    categories[product.category] = (categories[product.category] || 0) + 1
  })
  
  const total = myProducts.value.length
  return Object.entries(categories).map(([name, count]) => ({
    name,
    count,
    percentage: total > 0 ? (count / total) * 100 : 0
  }))
})

const monthlyRevenue = computed(() => {
  const months = {}
  salesHistory.value.forEach(sale => {
    const month = new Date(sale.created_at).toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short' 
    })
    months[month] = (months[month] || 0) + sale.total_price
  })
  
  return Object.entries(months).map(([month, revenue]) => ({
    month,
    revenue
  })).slice(-6)
})

const fetchUserProfile = async () => {
  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      router.push('/login')
      return
    }
    
    const response = await fetch('http://localhost:8000/api/auth/profile/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.ok) {
      user.value = await response.json()
      editForm.first_name = user.value.first_name || ''
      editForm.last_name = user.value.last_name || ''
    } else {
      router.push('/login')
    }
  } catch (error) {
    console.error('Error fetching profile:', error)
  }
}

const fetchMyProducts = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch('http://localhost:8000/api/marketplace/products/my/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      myProducts.value = Array.isArray(data) ? data : (data.results || [])
      stats.value.totalProducts = myProducts.value.length
    }
  } catch (error) {
    console.error('Error fetching products:', error)
    myProducts.value = []
  }
}

const fetchSalesHistory = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch('http://localhost:8000/api/marketplace/orders/my/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      salesHistory.value = Array.isArray(data) ? data : (data.results || [])
      stats.value.totalSold = salesHistory.value.filter(sale => sale.status === 'completed').length
      stats.value.totalRevenue = salesHistory.value
        .filter(sale => sale.status === 'completed')
        .reduce((sum, sale) => sum + (sale.total_price || 0), 0)
    }
  } catch (error) {
    console.error('Error fetching sales:', error)
    salesHistory.value = []
  }
}

const fetchPurchaseHistory = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch('http://localhost:8000/api/marketplace/orders/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      purchaseHistory.value = Array.isArray(data) ? data : (data.results || [])
    }
  } catch (error) {
    console.error('Error fetching purchases:', error)
    purchaseHistory.value = []
  }
}

const fetchChats = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch('http://localhost:8000/api/marketplace/chats/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      const chats = Array.isArray(data) ? data : (data.results || [])
      stats.value.activeChats = chats.length
    }
  } catch (error) {
    console.error('Error fetching chats:', error)
    stats.value.activeChats = 0
  }
}

const updateProfile = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch('http://localhost:8000/api/auth/profile/', {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(editForm)
    })
    
    if (response.ok) {
      const updatedUser = await response.json()
      user.value = updatedUser.user || updatedUser
      showEditModal.value = false
    }
  } catch (error) {
    console.error('Error updating profile:', error)
  }
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-BD').format(price)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const handleProductAdded = () => {
  showAddProductModal.value = false
  fetchMyProducts()
}

const editProduct = (product) => {
  selectedProduct.value = product
  showEditProductModal.value = true
}

const handleProductUpdated = () => {
  showEditProductModal.value = false
  selectedProduct.value = null
  fetchMyProducts()
}

const deleteProduct = (product) => {
  productToDelete.value = product
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  if (!productToDelete.value) return
  
  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch(`http://localhost:8000/api/marketplace/products/my/${productToDelete.value.id}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.ok) {
      showDeleteModal.value = false
      productToDelete.value = null
      fetchMyProducts()
    } else {
      alert('Error deleting product. Please try again.')
    }
  } catch (error) {
    console.error('Error deleting product:', error)
    alert('Error deleting product. Please try again.')
  }
}

onMounted(async () => {
  await Promise.all([
    fetchUserProfile(),
    fetchMyProducts(),
    fetchSalesHistory(),
    fetchPurchaseHistory(),
    fetchChats()
  ])
  loading.value = false
})
</script>
