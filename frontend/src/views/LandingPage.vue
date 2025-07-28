<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-100 to-slate-300">
    <!-- Hero Section -->
    <div class="pt-20 pb-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            PC <span class="text-blue-600">Parser</span>
          </h1>
          <p class="text-xl md:text-2xl text-gray-700 mb-8 max-w-3xl mx-auto">
            Your all-in-one PC component marketplace. Compare prices, find the best deals, and build your dream PC.
          </p>
          
          <!-- CTA Buttons -->
          <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <router-link 
              to="/components" 
              class="px-8 py-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium text-lg shadow-lg"
            >
              Browse Components
            </router-link>
            <router-link 
              v-if="!isLoggedIn"
              to="/register" 
              class="px-8 py-4 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium text-lg shadow-lg"
            >
              Get Started
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">Why Choose PC Parser?</h2>
          <p class="text-lg text-gray-600">Everything you need to build the perfect PC</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="text-center p-6">
            <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">Compare Prices</h3>
            <p class="text-gray-600">Find the best deals across multiple vendors and save money on your PC build.</p>
          </div>
          
          <div class="text-center p-6">
            <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">Smart Search</h3>
            <p class="text-gray-600">Advanced filtering and search capabilities to find exactly what you need.</p>
          </div>
          
          <div class="text-center p-6">
            <div class="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">Real-time Updates</h3>
            <p class="text-gray-600">Get the latest prices and availability information updated in real-time.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- API Status Section -->
    <div class="py-16 bg-gray-50">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div class="bg-white rounded-2xl shadow-xl p-8">
          <div v-if="loading" class="text-gray-500">Loading...</div>
          <div v-else>
            <p class="text-xl text-green-700 font-medium">Backend Status:</p>
            <p class="text-2xl mt-2 font-mono text-gray-800">{{ message }}</p>
          </div>
          <div class="mt-6">
            <button
              @click="fetchMessage"
              class="px-6 py-3 rounded-xl bg-blue-600 text-white hover:bg-blue-700 transition-colors font-medium"
            >
              Refresh Status
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const message = ref('')
const loading = ref(true)
const user = ref(null)

// Check if user is logged in
const isLoggedIn = computed(() => {
  return !!localStorage.getItem('access_token') && !!user.value
})

const fetchMessage = async () => {
  loading.value = true
  try {
    // Use this if using Vite proxy:
    const res = await axios.get('/api/auth/hello/')
    // If not using proxy, use the full URL:
    // const res = await axios.get('http://localhost:8000/api/auth/hello/')
    message.value = res.data.message
  } catch (error) {
    // If not authenticated, show a default message
    message.value = 'Hello from PC Parser!'
  } finally {
    loading.value = false
  }
}

const loadUserData = () => {
  const userData = localStorage.getItem('user')
  if (userData) {
    try {
      user.value = JSON.parse(userData)
    } catch (error) {
      console.error('Error parsing user data:', error)
      localStorage.removeItem('user')
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  }
}

const handleLogout = async () => {
  try {
    const refreshToken = localStorage.getItem('refresh_token')
    if (refreshToken) {
      await fetch('http://localhost:8000/api/auth/logout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({ refresh_token: refreshToken })
      })
    }
  } catch (error) {
    console.error('Logout error:', error)
  } finally {
    // Clear local storage regardless of API call success
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    user.value = null
    
    // Optionally redirect to login page
    // router.push('/login')
  }
}

onMounted(() => {
  loadUserData()
  fetchMessage()
})
</script>
