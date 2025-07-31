<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 to-blue-800 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div class="bg-white/10 backdrop-blur-md rounded-lg shadow-xl p-8 border border-white/20">
        <h2 class="text-center text-3xl font-extrabold text-white mb-8">Create Account</h2>
        <form @submit.prevent="handleRegister" class="space-y-6" enctype="multipart/form-data">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label for="first_name" class="block text-sm font-medium text-white mb-2">First Name</label>
              <input
                type="text"
                id="first_name"
                v-model="form.first_name"
                @blur="validateField('first_name')"
                :class="inputClass(errors.first_name)"
                placeholder="Enter your first name"
                required
              />
              <span v-if="errors.first_name" class="text-red-500 text-sm mt-1 block">{{ errors.first_name }}</span>
            </div>
            <div>
              <label for="last_name" class="block text-sm font-medium text-white mb-2">Last Name</label>
              <input
                type="text"
                id="last_name"
                v-model="form.last_name"
                @blur="validateField('last_name')"
                :class="inputClass(errors.last_name)"
                placeholder="Enter your last name"
                required
              />
              <span v-if="errors.last_name" class="text-red-500 text-sm mt-1 block">{{ errors.last_name }}</span>
            </div>
          </div>

          <div>
            <label for="username" class="block text-sm font-medium text-white mb-2">Username</label>
            <input
              type="text"
              id="username"
              v-model="form.username"
              @blur="validateField('username')"
              :class="inputClass(errors.username)"
              placeholder="Choose a username"
              required
            />
            <span v-if="errors.username" class="text-red-500 text-sm mt-1 block">{{ errors.username }}</span>
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-white mb-2">Email Address</label>
            <input
              type="email"
              id="email"
              v-model="form.email"
              @blur="validateField('email')"
              :class="inputClass(errors.email)"
              placeholder="Enter your email"
              required
            />
            <span v-if="errors.email" class="text-red-500 text-sm mt-1 block">{{ errors.email }}</span>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-white mb-2">Password</label>
            <input
              type="password"
              id="password"
              v-model="form.password"
              @blur="validateField('password')"
              :class="inputClass(errors.password)"
              placeholder="Create a password"
              required
            />
            <span v-if="errors.password" class="text-red-500 text-sm mt-1 block">{{ errors.password }}</span>
          </div>

          <div>
            <label for="password_confirm" class="block text-sm font-medium text-white mb-2">Confirm Password</label>
            <input
              type="password"
              id="password_confirm"
              v-model="form.password_confirm"
              @blur="validateField('password_confirm')"
              :class="inputClass(errors.password_confirm)"
              placeholder="Confirm your password"
              required
            />
            <span v-if="errors.password_confirm" class="text-red-500 text-sm mt-1 block">{{ errors.password_confirm }}</span>
          </div>

          <button 
            type="submit" 
            :disabled="loading || !isFormValid"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {{ loading ? 'Creating Account...' : 'Create Account' }}
          </button>
        </form>

        <div v-if="message" :class="[
          'mt-4 p-3 rounded-md text-center text-sm',
          messageType === 'success' ? 'bg-green-100 text-green-800 border border-green-200' : 'bg-red-100 text-red-800 border border-red-200'
        ]">
          {{ message }}
        </div>

        <div class="mt-6 text-center">
          <p class="text-sm text-white">
            Already have an account? 
            <router-link to="/login" class="text-white hover:text-blue-500 font-medium">Login</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(false)
const message = ref('')
const messageType = ref('')

const form = reactive({
  first_name: '',
  last_name: '',
  username: '',
  email: '',
  password: '',
  password_confirm: ''
})

const errors = reactive({})

const inputClass = (errorField) => [
  'w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500',
  errorField ? 'border-red-500' : 'border-gray-300'
]

const isFormValid = computed(() => {
  return Object.values(errors).every(e => !e)
})

const validateField = (field) => {
  switch (field) {
    case 'email':
      errors.email = !form.email.includes('@') ? 'Invalid email' : ''
      break
    case 'password':
      errors.password = form.password.length < 8 ? 'Password too short' : ''
      break
    case 'password_confirm':
      errors.password_confirm = form.password !== form.password_confirm ? 'Passwords do not match' : ''
      break
    default:
      errors[field] = !form[field] ? 'Required' : ''
  }
}

const handleRegister = async () => {
  Object.keys(form).forEach(validateField)
  if (!isFormValid.value) return

  loading.value = true
  try {
    const response = await fetch('http://localhost:8000/api/auth/register/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    })
    const data = await response.json()
    if (response.ok) {
      message.value = data.message || 'Registration successful.'
      messageType.value = 'success'
      setTimeout(() => router.push('/verify-email'), 2000)
    } else {
      Object.assign(errors, data)
      messageType.value = 'error'
    }
  } catch {
    message.value = 'Something went wrong. Please try again.'
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}
</script>
