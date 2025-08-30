<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <nav class="bg-white shadow-lg border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo and Brand -->
        <div class="flex items-center">
          <router-link to="/" class="flex items-center">
            <img :src="pcLogo" alt="PC Parser Logo" class="w-35 h-35 object-contain" />
          </router-link>
        </div>

        <div class="hidden md:flex items-center space-x-8">
          <router-link
            to="/"
            class="text-gray-700 hover:text-blue-600 transition-colors font-medium"
            :class="{ 'text-blue-600 font-bold': $route.path === '/' }"
          >
            Home
          </router-link>

          <router-link
            to="/about"
            class="text-gray-700 hover:text-blue-600 transition-colors font-medium"
            :class="{ 'text-blue-600 font-bold': $route.path === '/about' }"
          >
            About
          </router-link>

          <div ref="componentsDropdown" class="relative">
            <span
              @click="toggleComponentsDropdown"
              class="cursor-pointer text-gray-700 hover:text-blue-600 transition-colors font-medium select-none"
              :class="{ 'text-blue-600 font-bold': $route.path.startsWith('/components') }"
            >
              Components
            </span>
            <div
              v-show="showComponentsDropdown"
              class="absolute left-0 mt-2 w-56 bg-white rounded-lg shadow-lg z-50 transition-all duration-300"
            >
              <ul class="divide-y divide-gray-200">
                <li>
                  <router-link to="/components/monitor" class="block px-4 py-2 hover:bg-gray-100"
                    >Monitor</router-link
                  >
                </li>
                <li>
                  <router-link to="/components/cpu" class="block px-4 py-2 hover:bg-gray-100"
                    >CPUs</router-link
                  >
                </li>
                <li>
                  <router-link to="/components/storage" class="block px-4 py-2 hover:bg-gray-100"
                    >Storage</router-link
                  >
                </li>
                <li>
                  <router-link
                    to="/components/power-supplies"
                    class="block px-4 py-2 hover:bg-gray-100"
                    >Power Supplies</router-link
                  >
                </li>
                <li>
                  <router-link to="/components/cases" class="block px-4 py-2 hover:bg-gray-100"
                    >Cases</router-link
                  >
                </li>
                <li>
                  <router-link to="/components/memory" class="block px-4 py-2 hover:bg-gray-100"
                    >Memory</router-link
                  >
                </li>
                <li>
                  <router-link
                    to="/components/motherboards"
                    class="block px-4 py-2 hover:bg-gray-100"
                    >Motherboards</router-link
                  >
                </li>
                <li>
                  <router-link to="/components/gpu" class="block px-4 py-2 hover:bg-gray-100"
                    >GPU</router-link
                  >
                </li>
              </ul>
            </div>
          </div>

          <router-link
            to="/builder"
            class="text-gray-700 hover:text-blue-600 transition-colors font-medium"
            :class="{ 'text-blue-600 font-bold': $route.path === '/builder' }"
          >
            Builder
          </router-link>

          <router-link
            to="/marketplace"
            class="text-gray-700 hover:text-blue-600 transition-colors font-medium"
            :class="{ 'text-blue-600 font-bold': $route.path === '/marketplace' }"
          >
            Marketplace
          </router-link>
        </div>

        <!-- User Section -->
        <div class="flex items-center space-x-4">
          <!-- Marketplace Cart -->
          <CartDropdown v-if="isLoggedIn && isInMarketplace" />
          
          <!-- Authenticated User -->
          <div v-if="isLoggedIn && user" class="flex items-center space-x-3">
            <span class="hidden sm:block text-sm text-gray-600">
              Welcome, {{ user.first_name }}!
            </span>
            <UserAvatar :user="user" @logout="handleLogout" />
          </div>

          <!-- Guest User -->
          <div v-else class="flex items-center space-x-3">
            <router-link
              to="/login"
              class="text-gray-600 hover:text-blue-600 transition-colors font-medium"
            >
              Login
            </router-link>
            <router-link
              to="/register"
              class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              Sign Up
            </router-link>
          </div>

          <!-- Mobile Menu Button -->
          <button
            @click="toggleMobileMenu"
            class="md:hidden p-2 rounded-md text-gray-600 hover:text-blue-600 hover:bg-gray-100 transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                v-if="!showMobileMenu"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
              <path
                v-else
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile Menu -->
      <div v-if="showMobileMenu" class="md:hidden border-t border-gray-200 py-4">
        <div class="flex flex-col space-y-3">
          <router-link
            to="/"
            @click="closeMobileMenu"
            class="text-gray-600 hover:text-blue-600 transition-colors font-medium px-2 py-1"
            :class="{ 'text-blue-600': $route.path === '/' }"
          >
            Home
          </router-link>
          <router-link
            to="/components"
            @click="closeMobileMenu"
            class="text-gray-600 hover:text-blue-600 transition-colors font-medium px-2 py-1"
            :class="{ 'text-blue-600': $route.path.startsWith('/components') }"
          >
            Components
          </router-link>

          <!-- Mobile Auth Links -->
          <div v-if="!isLoggedIn" class="border-t border-gray-200 pt-3 mt-3">
            <router-link
              to="/login"
              @click="closeMobileMenu"
              class="block text-gray-600 hover:text-blue-600 transition-colors font-medium px-2 py-1"
            >
              Login
            </router-link>
            <router-link
              to="/register"
              @click="closeMobileMenu"
              class="block bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium mt-2"
            >
              Sign Up
            </router-link>
          </div>

          <!-- Mobile User Info -->
          <div v-else class="border-t border-gray-200 pt-3 mt-3">
            <div class="flex items-center space-x-3 px-2 py-1">
              <div class="w-8 h-8 rounded-full overflow-hidden">
                <img
                  v-if="user?.profile_image_url"
                  :src="user.profile_image_url"
                  :alt="`${user.first_name} ${user.last_name}`"
                  class="w-full h-full object-cover"
                />
                <div
                  v-else
                  class="w-full h-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-semibold text-xs"
                >
                  {{ getInitials() }}
                </div>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-900">
                  {{ user?.first_name }} {{ user?.last_name }}
                </p>
                <p class="text-xs text-gray-500">
                  {{ user?.email }}
                </p>
              </div>
            </div>
            <button
              @click="handleLogout"
              class="block w-full text-left text-red-600 hover:bg-red-50 transition-colors font-medium px-2 py-1 mt-2"
            >
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, watch, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import UserAvatar from './UserAvatar.vue'
import CartDropdown from './CartDropdown.vue'
import pcLogo from '@/assets/Images/PC Parser logo.png'

const router = useRouter()
const route = useRoute()
const user = ref(null)
const showMobileMenu = ref(false)
const accessToken = ref(localStorage.getItem('access_token'))
const showComponentsDropdown = ref(false)
const componentsDropdown = ref(null)

const isInMarketplace = computed(() => {
  return route.path.startsWith('/marketplace')
})

watch(accessToken, (newToken) => {
  if (newToken) {
    loadUserData()
  } else {
    user.value = null
  }
})

const isLoggedIn = computed(() => {
  return !!accessToken.value && !!user.value
})

const getInitials = () => {
  if (!user.value) return '?'
  const firstName = user.value.first_name || ''
  const lastName = user.value.last_name || ''
  return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase()
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
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({ refresh_token: refreshToken }),
      })
    }
  } catch (error) {
    console.error('Logout error:', error)
  } finally {
    
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    user.value = null

    closeMobileMenu()
    router.push('/')
  }
}

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const closeMobileMenu = () => {
  showMobileMenu.value = false
}

const toggleComponentsDropdown = () => {
  showComponentsDropdown.value = !showComponentsDropdown.value
}

const handleClickOutsideDropdown = (e) => {
  if (componentsDropdown.value && !componentsDropdown.value.contains(e.target)) {
    showComponentsDropdown.value = false
  }
}

onMounted(() => {
  loadUserData()

  document.addEventListener('click', handleClickOutsideDropdown)

  window.addEventListener('storage', (e) => {
    if (e.key === 'user' || e.key === 'access_token') {
      loadUserData()
    }
  })

  window.addEventListener('userLoggedIn', () => {
    accessToken.value = localStorage.getItem('access_token')
    loadUserData()
  })
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutsideDropdown)
})
</script>
