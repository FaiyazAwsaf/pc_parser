<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-slate-100 to-slate-300"
  >
    <div class="bg-white rounded-2xl shadow-xl p-8 max-w-md text-center">
      <h1 class="text-3xl font-bold mb-4 text-blue-700">PC Parser</h1>
      <p class="text-lg text-gray-700 mb-8">Your all-in-one PC component marketplace</p>
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
import { ref, onMounted } from 'vue'
import axios from 'axios'

const message = ref('')
const loading = ref(true)

const fetchMessage = async () => {
  loading.value = true
  try {
    // Use this if using Vite proxy:
    const res = await axios.get('/api/hello/')
    // If not using proxy, use the full URL:
    // const res = await axios.get('http://localhost:8000/api/user/hello/')
    message.value = res.data.message
  } catch (error) {
    message.value = 'Failed to fetch message.'
  } finally {
    loading.value = false
  }
}

onMounted(fetchMessage)
</script>
