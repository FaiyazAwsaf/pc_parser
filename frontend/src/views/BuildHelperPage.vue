<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 to-blue-800 text-white flex flex-col">
    <main class="flex-1 flex items-center justify-center px-4 py-16">
      <div class="bg-white text-slate-900 w-full max-w-4xl rounded-3xl shadow-lg p-6 sm:p-10">
        <h1 class="text-2xl sm:text-3xl font-extrabold text-center mb-4">Build Your PC with AI</h1>
        <p class="text-center text-gray-500 mb-6">
          Ask anything about building your PC your AI assistant is ready!
        </p>

        <!-- Chat Box -->
        <div
          class="border border-gray-300 rounded-lg p-4 h-[400px] overflow-y-auto mb-4 bg-gray-50"
        >
          <div v-for="(msg, idx) in messages" :key="idx" class="mb-2">
            <div v-if="msg.type === 'user'" class="text-right">
              <span class="inline-block bg-blue-500 text-white px-3 py-2 rounded-lg max-w-xs">
                {{ msg.text }}
              </span>
            </div>
            <div v-else class="text-left">
              <span
                class="inline-block bg-gray-200 text-gray-800 px-3 py-2 rounded-lg max-w-xs whitespace-pre-wrap"
              >
                {{ msg.text }}
              </span>
            </div>
          </div>

          <!-- Loading indicator -->
          <div v-if="isLoading" class="text-left">
            <span class="inline-block bg-gray-200 text-gray-800 px-3 py-2 rounded-lg">
              Thinking...
            </span>
          </div>
        </div>

        <!-- Input -->
        <form @submit.prevent="sendMessage" class="flex gap-2">
          <input
            v-model="userInput"
            type="text"
            placeholder="Ask your build assistant..."
            class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            :disabled="isLoading"
          />
          <button
            type="submit"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
            :disabled="isLoading"
          >
            Send
          </button>
        </form>

        <!-- Prompt Suggestions -->
        <div class="mt-6">
          <p class="text-sm text-gray-600 font-semibold mb-2">Suggestions:</p>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="s in suggestions"
              :key="s"
              @click="userInput = s"
              class="px-3 py-1 rounded-full border text-sm hover:bg-blue-100"
              :disabled="isLoading"
            >
              {{ s }}
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const userInput = ref('')
const isLoading = ref(false)
const messages = ref([
  {
    type: 'ai',
    text: 'Hi! I am your PC build assistant. Ask me anything like "Build me a PC for gaming under 100k BDT"',
  },
])

const suggestions = [
  'Build a gaming PC under 100k BDT',
  'Suggest parts for a programming rig',
  'Give me a silent build for office use',
  'Best budget GPU for 1080p gaming',
]

const sendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value) return

  const userMessage = userInput.value
  messages.value.push({ type: 'user', text: userMessage })
  userInput.value = ''
  isLoading.value = true

  try {
    console.log('Sending request to:', '/api/builder/llmchat/')
    console.log('Message:', userMessage)

    const res = await axios.post('/api/builder/llmchat/', {
      message: userMessage,
    })

    console.log('Response:', res.data)
    messages.value.push({ type: 'ai', text: res.data.response })
  } catch (error) {
    console.error('Full error:', error)

    let errorMessage = 'Error connecting to AI backend.'

    if (error.response) {
      // Server responded with error status
      console.error('Response data:', error.response.data)
      console.error('Response status:', error.response.status)

      if (error.response.data && error.response.data.error) {
        errorMessage = `Server Error: ${error.response.data.error}`
        if (error.response.data.details) {
          errorMessage += `\n\nDetails: ${error.response.data.details}`
        }
      } else {
        errorMessage = `Server Error (${error.response.status}): ${error.response.statusText}`
      }
    } else if (error.request) {
      // Request was made but no response received
      errorMessage = 'No response from server. Make sure Django backend is running on port 8000.'
    } else {
      // Something else happened
      errorMessage = `Request Error: ${error.message}`
    }

    messages.value.push({ type: 'ai', text: errorMessage })
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
input::placeholder {
  color: #a0aec0;
}
</style>
