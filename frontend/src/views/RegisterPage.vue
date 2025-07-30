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
                :class="[
                  'w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500',
                  errors.first_name ? 'border-red-500' : 'border-gray-300'
                ]"
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
                :class="[
                  'w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500',
                  errors.last_name ? 'border-red-500' : 'border-gray-300'
                ]"
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
              :class="[
                'w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500',
                errors.username ? 'border-red-500' : 'border-gray-300'
              ]"
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
              :class="[
                'w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500',
                errors.email ? 'border-red-500' : 'border-gray-300'
              ]"
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
              :class="[
                'w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500',
                errors.password ? 'border-red-500' : 'border-gray-300'
              ]"
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
              :class="[
                'w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500',
                errors.password_confirm ? 'border-red-500' : 'border-gray-300'
              ]"
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
// Use your validated form logic here — imported or created as helper functions
// Add validators or use functions from your second RegisterPage to perform real-time field validation, confirm passwords, etc.
</script>
