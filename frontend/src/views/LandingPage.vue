<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 to-blue-800 text-white flex flex-col">
    <!-- Hero Section -->
    <section class="flex-1 flex flex-col justify-center items-center text-center pt-16 pb-16">
      <div class="max-w-6xl w-full flex flex-col lg:flex-row items-center justify-between px-6 gap-10">
        <!-- Image in the middle -->
        <div class="flex-1 flex justify-center lg:justify-center">
          <img src="@/assets/Images/Pcbuild.png" alt="PC Build Visual" class="w-full max-w-md rounded-xl shadow-2xl" />
        </div>

        <!-- Writeup on the right -->
        <div class="flex-1 text-center lg:text-left">
          <h1 class="text-3xl md:text-5xl font-extrabold tracking-tight mb-6 drop-shadow-xl">
            <span class="text-blue-400 animate-pulse">Choose Your Parts. Build Your PC</span>
          </h1>
          <p class="max-w-xl text-xl md:text-2xl mb-10 opacity-90 font-medium mx-auto lg:mx-0">
            Discover, compare &amp; build your perfect PC.<br />
            <span class="text-blue-200">
              Bangladesh’s most advanced PC component marketplace &amp; build assistant.
            </span>
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start items-center">
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
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="bg-white text-slate-900 py-20 shadow-inner rounded-t-3xl">
      <div class="max-w-6xl mx-auto px-4">
        <h2 class="text-3xl md:text-4xl font-extrabold text-center mb-4">
          Everything For Your PC, One Platform
        </h2>
        <p class="text-center text-lg mb-14 text-slate-600">
          No more tab chaos. All PC parts &amp; deals. One search.
        </p>
        <div class="grid md:grid-cols-3 gap-8">
          <!-- Feature: Price Comparison -->
          <div
            class="bg-gradient-to-tr from-blue-50 to-blue-100 rounded-2xl shadow-xl p-8 text-center group hover:scale-105 transition-transform duration-300 cursor-pointer"
            @click="toggleProductDropdown"
          >
            <svg class="mx-auto mb-4 w-12 h-12 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 17v-2a4 4 0 014-4h14" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 21v-2a4 4 0 014-4h14" />
              <circle cx="7" cy="7" r="4" stroke="currentColor" stroke-width="2" fill="none" />
            </svg>
            <h3 class="font-semibold text-xl mb-2">Live Price Comparison</h3>
            <p class="text-gray-600 group-hover:text-blue-600">
              Track and compare the latest prices on new &amp; used PC components from all major vendors in Bangladesh.
            </p>
          </div>

          <!-- Feature: Build Assistant -->
          <div @click="router.push('/builder')" class="bg-gradient-to-tr from-green-50 to-green-100 rounded-2xl shadow-xl p-8 text-center group hover:scale-105 transition-transform duration-300 cursor-pointer">
            <svg class="mx-auto mb-4 w-12 h-12 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            <h3 class="font-semibold text-xl mb-2">AI Build Helper</h3>
            <p class="text-gray-600 group-hover:text-green-600">
              Tell us your budget &amp; needs. Instantly get compatible, optimized builds for gaming, work, or study powered by AI!
            </p>
          </div>

          <!-- Feature: Second-hand Marketplace -->
          <div class="bg-gradient-to-tr from-purple-50 to-purple-100 rounded-2xl shadow-xl p-8 text-center group hover:scale-105 transition-transform duration-300">
            <svg class="mx-auto mb-4 w-12 h-12 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h8" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v8" />
            </svg>
            <h3 class="font-semibold text-xl mb-2">Trusted Used Market</h3>
            <p class="text-gray-600 group-hover:text-purple-600">
              Browse verified, trustworthy second-hand parts buy and sell with confidence, no more marketplace scams.
            </p>
          </div>
        </div>

        <!-- Product Dropdown -->
        <transition name="fade">
          <div
            v-if="showProductDropdown"
            class="grid grid-cols-2 sm:grid-cols-4 gap-6 mt-10 px-4 sm:px-0 mx-auto max-w-5xl"
          >
            <div
              v-for="item in productItems"
              :key="item.label"
              class="flex flex-col items-center bg-gray-50 hover:bg-gray-100 rounded-lg p-5 shadow"
            >
              <img :src="item.image" alt="" class="w-16 h-16 object-contain mb-2" />
              <p class="text-base font-semibold text-gray-800 text-center">{{ item.label }}</p>
            </div>
          </div>
        </transition>
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

import cpuImg from '@/assets/Images/CPU.png'
import monitorImg from '@/assets/Images/Monitor.png'
import motherboardImg from '@/assets/Images/Motherboard.png'
import memoryImg from '@/assets/Images/Memory.png'
import storageImg from '@/assets/Images/Storage.png'
import gpuImg from '@/assets/Images/GPU.png'
import powersupplyImg from '@/assets/Images/Powersupply.png'
import caseImg from '@/assets/Images/Cases.png'

const router = useRouter()
const message = ref('')
const loading = ref(true)
const showProductDropdown = ref(false)
const user = ref(null)

const toggleProductDropdown = () => {
  showProductDropdown.value = !showProductDropdown.value
}

const isLoggedIn = computed(() => {
  return !!localStorage.getItem('access_token') && !!user.value
})

const productItems = [
  { label: 'CPUs', image: cpuImg },
  { label: 'Monitor', image: monitorImg },
  { label: 'Motherboards', image: motherboardImg },
  { label: 'Power Supplies', image: powersupplyImg },
  { label: 'Memory', image: memoryImg },
  { label: 'Storage', image: storageImg },
  { label: 'GPU', image: gpuImg },
  { label: 'Cases', image: caseImg }
]

const fetchMessage = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/auth/hello/')
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
    } catch {
      localStorage.clear()
    }
  }
}

onMounted(() => {
  loadUserData()
  fetchMessage()
})
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>
