<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 to-blue-800 text-white flex flex-col">
    <!-- Hero Section -->
    <section class="flex-1 flex flex-col justify-center items-center text-center pt-24 pb-16">
      <h1 class="text-5xl md:text-7xl font-extrabold tracking-tight mb-6 drop-shadow-xl">
        <span class="text-blue-400 animate-pulse">PC Parser</span>
      </h1>
      <p class="max-w-2xl text-xl md:text-2xl mb-10 opacity-90 font-medium">
        Discover, compare &amp; build your perfect PC.<br>
        <span class="text-blue-200">Bangladesh’s most advanced PC component marketplace &amp; build assistant.</span>
      </p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
        <router-link
          to="/components"
          class="px-8 py-4 rounded-full bg-blue-500 hover:bg-blue-600 shadow-lg text-white font-semibold text-lg transition-all duration-300"
        >
          Browse Components
        </router-link>
        <router-link
          v-if="!isLoggedIn"
          to="/register"
          class="px-8 py-4 rounded-full bg-green-500 hover:bg-green-600 shadow-lg text-white font-semibold text-lg transition-all duration-300"
        >
          Get Started
        </router-link>
      </div>
    </section>

    <!-- Features Section -->
    <section class="bg-white text-slate-900 py-20 shadow-inner rounded-t-3xl">
      <div class="max-w-6xl mx-auto px-4">
        <h2 class="text-3xl md:text-4xl font-extrabold text-center mb-4">Everything For Your PC, One Platform</h2>
        <p class="text-center text-lg mb-14 text-slate-600">No more tab chaos. All PC parts &amp; deals. One search.</p>
        <div class="grid md:grid-cols-3 gap-8">
          <!-- Feature: Price Comparison -->
          <div class="bg-gradient-to-tr from-blue-50 to-blue-100 rounded-2xl shadow-xl p-8 text-center group hover:scale-105 transition-transform duration-300">
            <svg class="mx-auto mb-4 w-12 h-12 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 17v-2a4 4 0 014-4h14" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 21v-2a4 4 0 014-4h14" />
              <circle cx="7" cy="7" r="4" stroke="currentColor" stroke-width="2" fill="none"/>
            </svg>
            <h3 class="font-semibold text-xl mb-2">Live Price Comparison</h3>
            <p class="text-gray-600 group-hover:text-blue-600">Track and compare the latest prices on new &amp; used PC components from all major vendors in Bangladesh.</p>
          </div>
          <!-- Feature: Build Assistant -->
          <div class="bg-gradient-to-tr from-green-50 to-green-100 rounded-2xl shadow-xl p-8 text-center group hover:scale-105 transition-transform duration-300">
            <svg class="mx-auto mb-4 w-12 h-12 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            <h3 class="font-semibold text-xl mb-2">AI Build Helper</h3>
            <p class="text-gray-600 group-hover:text-green-600">Tell us your budget &amp; needs. Instantly get compatible, optimized builds for gaming, work, or study powered by AI!</p>
          </div>
          <!-- Feature: Second-hand Marketplace -->
          <div class="bg-gradient-to-tr from-purple-50 to-purple-100 rounded-2xl shadow-xl p-8 text-center group hover:scale-105 transition-transform duration-300">
            <svg class="mx-auto mb-4 w-12 h-12 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h8" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v8" />
            </svg>
            <h3 class="font-semibold text-xl mb-2">Trusted Used Market</h3>
            <p class="text-gray-600 group-hover:text-purple-600">Browse verified, trustworthy second-hand parts buy and sell with confidence, no more marketplace scams.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- API Status Section (Demo backend health check) -->
    <section class="py-16 bg-slate-50 flex-1">
      <div class="max-w-3xl mx-auto px-4 text-center">
        <div class="bg-white rounded-2xl shadow-lg p-8">
          <div v-if="loading" class="text-gray-500 flex items-center justify-center gap-2">
            <svg class="w-6 h-6 animate-spin text-blue-500" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
            </svg>
            Loading backend status...
          </div>
          <div v-else>
            <p class="text-xl text-green-700 font-medium mb-1">Backend Status:</p>
            <p class="text-2xl mt-2 font-mono text-gray-800">{{ message }}</p>
          </div>
          <div class="mt-8">
            <button
              @click="fetchMessage"
              class="px-6 py-3 rounded-xl bg-blue-500 text-white hover:bg-blue-600 transition-colors font-medium shadow-md"
            >
              Refresh Status
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="py-6 text-center text-gray-400 bg-slate-900 mt-auto">
      &copy; {{ new Date().getFullYear() }} PC Parser. Crafted for PC lovers in Bangladesh 🇧🇩
    </footer>
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
    // If using Vite proxy:
    const res = await axios.get('/api/auth/hello/')
    // Otherwise:
    // const res = await axios.get('http://localhost:8000/api/auth/hello/')
    message.value = res.data.message
  } catch (error) {
    message.value = 'Unable to reach backend. Please try again later.'
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
      localStorage.removeItem('user')
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  }
}

onMounted(() => {
  loadUserData()
  fetchMessage()
})
</script>
