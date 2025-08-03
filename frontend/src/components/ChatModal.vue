<template>
  <div class="modal-overlay" @click="handleOverlayClick">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>Chat about {{ product.name }}</h2>
        <button @click="$emit('close')" class="close-btn">&times;</button>
      </div>
      
      <div class="chat-container">
        <div class="chat-messages" ref="messagesContainer">
          <div
            v-for="message in messages"
            :key="message.id"
            :class="['message', { 'own-message': message.sender === currentUser.id }]"
          >
            <div class="message-sender">{{ message.sender_name }}</div>
            <div class="message-content">{{ message.content }}</div>
            <div class="message-time">{{ formatTime(message.created_at) }}</div>
          </div>
          
          <div v-if="messages.length === 0" class="no-messages">
            No messages yet. Start the conversation!
          </div>
        </div>
        
        <div class="chat-input">
          <form @submit.prevent="sendMessage" class="message-form">
            <input
              v-model="newMessage"
              type="text"
              placeholder="Type your message..."
              :disabled="loading"
              class="message-input"
            />
            <button type="submit" :disabled="!newMessage.trim() || loading" class="send-btn">
              Send
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue'

export default {
  name: 'ChatModal',
  props: {
    product: {
      type: Object,
      required: true
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const messages = ref([])
    const newMessage = ref('')
    const loading = ref(false)
    const chatId = ref(null)
    const messagesContainer = ref(null)
    const currentUser = ref({})
    
    const initializeChat = async () => {
      try {
        // Get current user info
        const token = localStorage.getItem('access_token')
        console.log('Token:', token ? 'Present' : 'Missing')
        console.log('Full token:', token)
        
        const userResponse = await fetch('http://localhost:8000/api/auth/profile/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        
        console.log('User response status:', userResponse.status)
        
        if (userResponse.ok) {
          currentUser.value = await userResponse.json()
          console.log('Current user:', currentUser.value)
        } else {
          console.error('Failed to get user profile:', await userResponse.text())
          return
        }
        
        // Create or get chat
        const chatResponse = await fetch(`http://localhost:8000/api/marketplace/products/${props.product.id}/chat/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
        
        console.log('Chat response status:', chatResponse.status)
        
        if (chatResponse.ok) {
          const chatData = await chatResponse.json()
          console.log('Chat data:', chatData)
          chatId.value = chatData.id
          await loadMessages()
        } else {
          console.error('Failed to create/get chat:', await chatResponse.text())
        }
      } catch (error) {
        console.error('Error initializing chat:', error)
      }
    }
    
    const loadMessages = async () => {
      if (!chatId.value) return
      
      try {
        const token = localStorage.getItem('access_token')
        const response = await fetch(`http://localhost:8000/api/marketplace/chats/${chatId.value}/messages/`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        
        if (response.ok) {
          const data = await response.json()
          messages.value = data.results || data
          await nextTick()
          scrollToBottom()
        }
      } catch (error) {
        console.error('Error loading messages:', error)
      }
    }
    
    const sendMessage = async () => {
      if (!newMessage.value.trim() || !chatId.value) return
      
      loading.value = true
      
      try {
        const token = localStorage.getItem('access_token')
        const response = await fetch(`http://localhost:8000/api/marketplace/chats/${chatId.value}/messages/create/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            content: newMessage.value
          })
        })
        
        console.log('Send message response status:', response.status)
        
        if (response.ok) {
          newMessage.value = ''
          await loadMessages()
          console.log('Message sent successfully')
        } else {
          const errorText = await response.text()
          console.error('Failed to send message:', errorText)
        }
      } catch (error) {
        console.error('Error sending message:', error)
      } finally {
        loading.value = false
      }
    }
    
    const scrollToBottom = () => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    }
    
    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleTimeString()
    }
    
    const handleOverlayClick = () => {
      emit('close')
    }
    
    onMounted(() => {
      initializeChat()
    })
    
    return {
      messages,
      newMessage,
      loading,
      messagesContainer,
      currentUser,
      sendMessage,
      formatTime,
      handleOverlayClick
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  height: 70vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  color: #333;
  font-size: 18px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #333;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  max-height: calc(70vh - 140px);
}

.message {
  margin-bottom: 15px;
  padding: 10px;
  border-radius: 8px;
  background: #f8f9fa;
}

.message.own-message {
  background: #007bff;
  color: white;
  margin-left: 20%;
}

.message-sender {
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 5px;
  opacity: 0.8;
}

.message-content {
  margin-bottom: 5px;
}

.message-time {
  font-size: 11px;
  opacity: 0.6;
}

.no-messages {
  text-align: center;
  color: #666;
  font-style: italic;
  margin-top: 50px;
}

.chat-input {
  padding: 20px;
  border-top: 1px solid #eee;
}

.message-form {
  display: flex;
  gap: 10px;
}

.message-input {
  flex: 1;
  padding: 10px;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
}

.message-input:focus {
  outline: none;
  border-color: #007bff;
}

.send-btn {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.send-btn:hover:not(:disabled) {
  background: #0056b3;
}

.send-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    height: 80vh;
  }
  
  .message.own-message {
    margin-left: 10%;
  }
}
</style>
