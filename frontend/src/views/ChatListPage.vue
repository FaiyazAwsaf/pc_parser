<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-4xl mx-auto">
      <div class="bg-white rounded-lg shadow-md">
        <div class="border-b border-gray-200 px-6 py-4">
          <h1 class="text-2xl font-bold text-gray-800">My Chats</h1>
          <p class="text-gray-600 mt-1">View and manage your conversations</p>
        </div>

        <div v-if="loading" class="flex justify-center items-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-700"></div>
        </div>

        <div v-else-if="chats.length === 0" class="text-center py-12">
          <div class="text-6xl mb-4">💬</div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">No conversations yet</h3>
          <p class="text-gray-500 mb-6">Start chatting with sellers about products you're interested in!</p>
          <router-link 
            to="/marketplace" 
            class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
          >
            Browse Marketplace
          </router-link>
        </div>

        <div v-else class="divide-y divide-gray-200">
          <div 
            v-for="chat in chats" 
            :key="chat.id"
            @click="openChat(chat)"
            class="p-6 hover:bg-gray-50 cursor-pointer transition-colors"
          >
            <div class="flex items-start space-x-4">
              <div class="flex-shrink-0">
                <div class="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold">
                  {{ getInitials(chat.seller_name) }}
                </div>
              </div>
              
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between mb-1">
                  <h3 class="text-lg font-medium text-gray-900 truncate">
                    {{ chat.product_name }}
                  </h3>
                  <span class="text-sm text-gray-500">
                    {{ formatTime(chat.last_message?.created_at || chat.created_at) }}
                  </span>
                </div>
                
                <p class="text-sm text-gray-600 mb-2">
                  Chat with {{ chat.seller_name }}
                </p>
                
                <div v-if="chat.last_message" class="flex items-center space-x-2">
                  <span class="text-sm font-medium text-gray-700">
                    {{ chat.last_message.sender }}:
                  </span>
                  <span class="text-sm text-gray-600 truncate">
                    {{ chat.last_message.content }}
                  </span>
                </div>
                
                <div v-else class="text-sm text-gray-500 italic">
                  No messages yet
                </div>
              </div>
              
              <div class="flex-shrink-0">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Chat Modal -->
    <div v-if="selectedChat" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg w-full max-w-4xl h-5/6 flex flex-col">
        <div class="flex items-center justify-between p-4 border-b border-gray-200">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold">
              {{ getInitials(selectedChat.seller_name) }}
            </div>
            <div>
              <h2 class="text-lg font-medium text-gray-900">{{ selectedChat.product_name }}</h2>
              <p class="text-sm text-gray-600">Chat with {{ selectedChat.seller_name }}</p>
            </div>
          </div>
          <button @click="closeChat" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <div class="flex-1 flex flex-col">
          <div class="flex-1 overflow-y-auto p-4" ref="messagesContainer">
            <div
              v-for="message in messages"
              :key="message.id"
              :class="['mb-4 flex', message.sender === currentUser.id ? 'justify-end' : 'justify-start']"
            >
              <div
                :class="[
                  'max-w-xs lg:max-w-md px-4 py-2 rounded-lg',
                  message.sender === currentUser.id
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-800'
                ]"
              >
                <div class="text-xs opacity-75 mb-1">{{ message.sender_name }}</div>
                <div>{{ message.content }}</div>
                <div class="text-xs opacity-75 mt-1">{{ formatTime(message.created_at) }}</div>
              </div>
            </div>
            
            <div v-if="messages.length === 0" class="text-center py-8">
              <div class="text-4xl mb-4">💬</div>
              <p class="text-gray-500">No messages yet. Start the conversation!</p>
            </div>
          </div>

          <div class="border-t border-gray-200 p-4">
            <form @submit.prevent="sendMessage" class="flex space-x-2">
              <input
                v-model="newMessage"
                type="text"
                placeholder="Type your message..."
                :disabled="sendingMessage"
                class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button
                type="submit"
                :disabled="!newMessage.trim() || sendingMessage"
                class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ sendingMessage ? 'Sending...' : 'Send' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(true)
const chats = ref([])
const selectedChat = ref(null)
const messages = ref([])
const newMessage = ref('')
const sendingMessage = ref(false)
const messagesContainer = ref(null)
const currentUser = ref({})

const fetchCurrentUser = async () => {
  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      router.push('/login')
      return
    }

    const response = await fetch('http://localhost:8000/api/auth/profile/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (response.ok) {
      currentUser.value = await response.json()
    } else {
      router.push('/login')
    }
  } catch (error) {
    console.error('Error fetching user profile:', error)
    router.push('/login')
  }
}

const fetchChats = async () => {
  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      router.push('/login')
      return
    }

    const response = await fetch('http://localhost:8000/api/marketplace/chats/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (response.ok) {
      const data = await response.json()
      chats.value = Array.isArray(data) ? data : (data.results || [])
      
      // Sort chats by last message time or creation time
      chats.value.sort((a, b) => {
        const aTime = a.last_message?.created_at || a.created_at
        const bTime = b.last_message?.created_at || b.created_at
        return new Date(bTime) - new Date(aTime)
      })
    } else {
      console.error('Failed to fetch chats')
    }
  } catch (error) {
    console.error('Error fetching chats:', error)
  } finally {
    loading.value = false
  }
}

const openChat = async (chat) => {
  selectedChat.value = chat
  await loadMessages(chat.id)
}

const closeChat = () => {
  selectedChat.value = null
  messages.value = []
  newMessage.value = ''
}

const loadMessages = async (chatId) => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch(`http://localhost:8000/api/marketplace/chats/${chatId}/messages/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (response.ok) {
      const data = await response.json()
      messages.value = Array.isArray(data) ? data : (data.results || [])
      await nextTick()
      scrollToBottom()
    }
  } catch (error) {
    console.error('Error loading messages:', error)
  }
}

const sendMessage = async () => {
  if (!newMessage.value.trim() || !selectedChat.value) return

  sendingMessage.value = true

  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch(`http://localhost:8000/api/marketplace/chats/${selectedChat.value.id}/messages/create/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        content: newMessage.value
      })
    })

    if (response.ok) {
      newMessage.value = ''
      await loadMessages(selectedChat.value.id)
      // Refresh the chat list to update last message
      await fetchChats()
    } else {
      console.error('Failed to send message')
    }
  } catch (error) {
    console.error('Error sending message:', error)
  } finally {
    sendingMessage.value = false
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const getInitials = (name) => {
  if (!name) return 'U'
  return name.split(' ').map(word => word.charAt(0)).join('').toUpperCase().slice(0, 2)
}

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  
  const date = new Date(timestamp)
  const now = new Date()
  const diffInHours = (now - date) / (1000 * 60 * 60)
  
  if (diffInHours < 24) {
    return date.toLocaleTimeString('en-US', { 
      hour: 'numeric', 
      minute: '2-digit',
      hour12: true 
    })
  } else if (diffInHours < 24 * 7) {
    return date.toLocaleDateString('en-US', { weekday: 'short' })
  } else {
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric' 
    })
  }
}

onMounted(async () => {
  await fetchCurrentUser()
  await fetchChats()
})
</script>
