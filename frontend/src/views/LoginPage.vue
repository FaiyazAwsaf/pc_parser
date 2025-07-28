<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div class="bg-white rounded-lg shadow-md p-8">
        <h2 class="text-center text-3xl font-extrabold text-gray-900 mb-8">Login to PC Parser</h2>
        
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
            <input
              type="email"
              id="email"
              v-model="form.email"
              :class="[
                'w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                errors.email ? 'border-red-500' : 'border-gray-300'
              ]"
              placeholder="Enter your email"
              required
            />
            <span v-if="errors.email" class="text-red-500 text-sm mt-1 block">{{ errors.email }}</span>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">Password</label>
            <input
              type="password"
              id="password"
              v-model="form.password"
              :class="[
                'w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                errors.password ? 'border-red-500' : 'border-gray-300'
              ]"
              placeholder="Enter your password"
              required
            />
            <span v-if="errors.password" class="text-red-500 text-sm mt-1 block">{{ errors.password }}</span>
          </div>

          <button 
            type="submit" 
            :disabled="loading"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {{ loading ? 'Logging in...' : 'Login' }}
          </button>
        </form>

        <div v-if="message" :class="[
          'mt-4 p-3 rounded-md text-center text-sm',
          messageType === 'success' ? 'bg-green-100 text-green-800 border border-green-200' : 'bg-red-100 text-red-800 border border-red-200'
        ]">
          {{ message }}
        </div>

        <div class="mt-6 text-center space-y-2">
          <p class="text-sm text-gray-600">
            Don't have an account? 
            <router-link to="/register" class="text-blue-600 hover:text-blue-500 font-medium">Create Account</router-link>
          </p>
          <p class="text-sm text-gray-600">
            Need to verify your email? 
            <router-link to="/verify-email" class="text-blue-600 hover:text-blue-500 font-medium">Verify Email</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(false)
const message = ref('')
const messageType = ref('')

const form = reactive({
  email: '',
  password: ''
})

const errors = reactive({
  email: '',
  password: ''
})

const clearErrors = () => {
  errors.email = ''
  errors.password = ''
  message.value = ''
}

const handleLogin = async () => {
  clearErrors()
  loading.value = true

  try {
    const response = await fetch('http://localhost:8000/api/auth/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form)
    })

    const data = await response.json()

    if (response.ok) {
      // Store tokens in localStorage
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
      localStorage.setItem('user', JSON.stringify(data.user))
      
      message.value = data.message
      messageType.value = 'success'
      
      // Redirect to dashboard or home page
      setTimeout(() => {
        router.push('/')
      }, 1500)
    } else {
      if (data.error) {
        message.value = data.error
        messageType.value = 'error'
        
        // If email not verified, show option to verify
        if (data.error.includes('Email not verified')) {
          setTimeout(() => {
            router.push('/verify-email')
          }, 2000)
        }
      } else {
        // Handle field-specific errors
        Object.keys(data).forEach(key => {
          if (errors.hasOwnProperty(key)) {
            errors[key] = Array.isArray(data[key]) ? data[key][0] : data[key]
          }
        })
      }
    }
  } catch (error) {
    message.value = 'Network error. Please try again.'
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}
</script>
