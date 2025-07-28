<template>
  <div class="user-avatar">
    <div class="relative">
      <!-- User Avatar Image -->
      <div 
        class="w-10 h-10 rounded-full overflow-hidden border-2 border-white shadow-lg cursor-pointer"
        @click="toggleDropdown"
      >
        <img 
          v-if="user?.profile_image_url" 
          :src="user.profile_image_url" 
          :alt="`${user.first_name} ${user.last_name}`"
          class="w-full h-full object-cover"
        />
        <div 
          v-else 
          class="w-full h-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-semibold text-sm"
        >
          {{ getInitials() }}
        </div>
      </div>

      <!-- Dropdown Menu -->
      <div 
        v-if="showDropdown" 
        class="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-xl border border-gray-200 z-50"
        @click.stop
      >
        <!-- User Info Section -->
        <div class="px-4 py-3 border-b border-gray-100">
          <div class="flex items-center space-x-3">
            <div class="w-12 h-12 rounded-full overflow-hidden">
              <img 
                v-if="user?.profile_image_url" 
                :src="user.profile_image_url" 
                :alt="`${user.first_name} ${user.last_name}`"
                class="w-full h-full object-cover"
              />
              <div 
                v-else 
                class="w-full h-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-semibold"
              >
                {{ getInitials() }}
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 truncate">
                {{ user?.first_name }} {{ user?.last_name }}
              </p>
              <p class="text-sm text-gray-500 truncate">
                {{ user?.email }}
              </p>
            </div>
          </div>
        </div>

        <!-- Menu Items -->
        <div class="py-1">
          <button
            @click="goToProfile"
            class="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
          >
            <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            View Profile
          </button>
          
          <button
            @click="goToSettings"
            class="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
          >
            <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Settings
          </button>
          
          <div class="border-t border-gray-100 my-1"></div>
          
          <button
            @click="handleLogout"
            class="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
          >
            <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            Sign Out
          </button>
        </div>
      </div>
    </div>

    <!-- Backdrop to close dropdown -->
    <div 
      v-if="showDropdown" 
      class="fixed inset-0 z-40" 
      @click="closeDropdown"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  user: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['logout'])

const router = useRouter()
const showDropdown = ref(false)

const getInitials = () => {
  if (!props.user) return '?'
  const firstName = props.user.first_name || ''
  const lastName = props.user.last_name || ''
  return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase()
}

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
}

const closeDropdown = () => {
  showDropdown.value = false
}

const goToProfile = () => {
  closeDropdown()
  router.push('/profile')
}

const goToSettings = () => {
  closeDropdown()
  router.push('/settings')
}

const handleLogout = async () => {
  closeDropdown()
  emit('logout')
}

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  if (!event.target.closest('.user-avatar')) {
    closeDropdown()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.user-avatar {
  position: relative;
}
</style>
