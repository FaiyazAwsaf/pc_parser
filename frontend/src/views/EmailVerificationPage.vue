<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 to-blue-800 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div class="bg-white/10 backdrop-blur-md rounded-lg shadow-xl p-8 border border-white/20">
        <h2 class="text-center text-3xl font-extrabold text-white mb-4">Verify Your Email</h2>
        <p class="text-center text-sm text-white opacity-90 mb-8 leading-relaxed">
          We've sent a 6-digit verification code to your email address. 
          Please enter it below to verify your account.
        </p>
        
        <form @submit.prevent="handleVerification" class="space-y-6">
          <div>
            <label for="email" class="block text-sm font-medium text-white mb-2">Email Address</label>
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
            <label for="token" class="block text-sm font-medium text-white mb-2">Verification Code</label>
            <input
              type="text"
              id="token"
              v-model="form.token"
              :class="[
                'w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-center text-lg font-semibold tracking-widest',
                errors.token ? 'border-red-500' : 'border-gray-300'
              ]"
              placeholder="Enter 6-digit code"
              maxlength="6"
              pattern="[0-9]{6}"
              required
            />
            <span v-if="errors.token" class="text-red-500 text-sm mt-1 block">{{ errors.token }}</span>
          </div>

          <button 
            type="submit" 
            :disabled="loading"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {{ loading ? 'Verifying...' : 'Verify Email' }}
          </button>
        </form>

        <div v-if="message" :class="[
          'mt-4 p-3 rounded-md text-center text-sm',
          messageType === 'success' ? 'bg-green-100 text-green-800 border border-green-200' : 'bg-red-100 text-red-800 border border-red-200'
        ]">
          {{ message }}
        </div>

        <div class="mt-6 text-center">
          <button 
            @click="resendCode" 
            :disabled="resendLoading || resendCooldown > 0"
            class="text-sm text-blue-300 hover:text-blue-400 font-medium underline disabled:text-gray-400 disabled:no-underline disabled:cursor-not-allowed"
          >
            {{ resendLoading ? 'Sending...' : resendCooldown > 0 ? `Resend in ${resendCooldown}s` : 'Resend Code' }}
          </button>
        </div>

        <div class="mt-6 text-center space-y-2">
          <p class="text-sm text-white">
            Remember your password? 
            <router-link to="/login" class="text-blue-300 hover:text-blue-400 font-medium">Login</router-link>
          </p>
          <p class="text-sm text-white">
            Need to create an account? 
            <router-link to="/register" class="text-blue-300 hover:text-blue-400 font-medium">Register</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const resendLoading = ref(false)
const message = ref('')
const messageType = ref('')
const resendCooldown = ref(0)
let cooldownInterval = null

const form = reactive({
  email: '',
  token: ''
})

const errors = reactive({
  email: '',
  token: ''
})

const clearErrors = () => {
  errors.email = ''
  errors.token = ''
  message.value = ''
}

const startCooldown = () => {
  resendCooldown.value = 60
  cooldownInterval = setInterval(() => {
    resendCooldown.value--
    if (resendCooldown.value <= 0) {
      clearInterval(cooldownInterval)
    }
  }, 1000)
}

const handleVerification = async () => {
  clearErrors()
  loading.value = true

  try {
    const response = await fetch('http://localhost:8000/api/auth/verify-email/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form)
    })

    const data = await response.json()

    if (response.ok) {
      message.value = data.message
      messageType.value = 'success'
      setTimeout(() => {
        router.push('/login')
      }, 2000)
    } else {
      if (data.error) {
        message.value = data.error
        messageType.value = 'error'
      } else {
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

const resendCode = async () => {
  if (!form.email) {
    message.value = 'Please enter your email address first.'
    messageType.value = 'error'
    return
  }

  clearErrors()
  resendLoading.value = true

  try {
    const response = await fetch('http://localhost:8000/api/auth/resend-verification/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email: form.email })
    })

    const data = await response.json()

    if (response.ok) {
      message.value = data.message
      messageType.value = 'success'
      startCooldown()
    } else {
      message.value = data.error || 'Failed to resend verification code.'
      messageType.value = 'error'
    }
  } catch (error) {
    message.value = 'Network error. Please try again.'
    messageType.value = 'error'
  } finally {
    resendLoading.value = false
  }
}

onMounted(() => {
  if (route.query.email) {
    form.email = route.query.email
  }
})

onUnmounted(() => {
  if (cooldownInterval) {
    clearInterval(cooldownInterval)
  }
})
</script>
