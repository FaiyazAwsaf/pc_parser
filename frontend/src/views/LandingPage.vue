<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-slate-100 to-slate-300"
  >
    <div class="bg-white rounded-2xl shadow-xl p-8 max-w-md text-center">
      <h1 class="text-3xl font-bold mb-4 text-blue-700">PC Parser</h1>
      <p class="text-lg text-gray-700 mb-8">Your all-in-one PC component marketplace</p>
      
      <!-- Authentication Buttons -->
      <div v-if="!isLoggedIn" class="mb-8 space-y-4">
        <div class="flex gap-4">
          <router-link 
            to="/login" 
            class="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            Login
          </router-link>
          <router-link 
            to="/register" 
            class="flex-1 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium"
          >
            Create Account
          </router-link>
        </div>
      </div>

      <!-- User Info (if logged in) -->
      <div v-else class="mb-8 p-4 bg-green-50 rounded-lg border border-green-200">
        <p class="text-green-800 font-medium">Welcome back, {{ user.first_name }}!</p>
        <p class="text-sm text-green-600 mt-1">{{ user.email }}</p>
        <button 
          @click="handleLogout"
          class="mt-3 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors text-sm"
        >
          Logout
        </button>
      </div>
      
      <div v-if="loading" class="text-gray-500">Loading...</div>
      <div v-else>
        <p class="text-xl text-green-700 font-medium">Backend says:</p>
        <p class="text-2xl mt-2 font-mono">{{ message }}</p>
      </div>
      <div class="mt-8">
        <button
          @click="fetchMessage"
          class="px-4 py-2 rounded-xl bg-blue-600 text-white hover:bg-blue-700 transition"
        >
          Refresh Message
        </button>
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
