<template>
  <div class="relative">
    <!-- Search Input -->
    <div class="relative">
      <input 
        ref="searchInput"
        v-model="searchQuery" 
        @input="handleInput"
        @keydown="handleKeydown"
        @focus="showSuggestions = true"
        @blur="handleBlur"
        type="text" 
        placeholder="Search for products, brands, categories..." 
        class="w-full px-4 py-3 pr-16 border border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:ring-opacity-50 transition-all duration-200 resize-none overflow-hidden"
        style="height: 48px; min-height: 48px; max-height: 48px;"
      >
      
      <!-- Search Icon -->
      <div class="absolute inset-y-0 right-0 flex items-center pr-3">
        <svg v-if="!loading" class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
        <div v-else class="animate-spin h-5 w-5 border-2 border-blue-500 border-t-transparent rounded-full"></div>
      </div>
      
      <!-- Search Button -->
      <button 
        @click="executeSearch"
        class="absolute inset-y-0 right-8 flex items-center pr-3 text-blue-600 hover:text-blue-800 transition"
        title="Search"
      >
        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5-5 5M6 12h12"></path>
        </svg>
      </button>
    </div>

    <!-- Suggestions Dropdown -->
    <div 
      v-if="showSuggestions && (suggestions.length > 0 || searchQuery.length >= 2)"
      class="absolute z-50 w-full mt-1 bg-white border border-gray-200 rounded-md shadow-lg max-h-96 overflow-y-auto"
    >
      <!-- Loading State -->
      <div v-if="loading && searchQuery.length >= 2" class="px-4 py-3 text-gray-500 text-center">
        <div class="flex items-center justify-center">
          <div class="animate-spin h-4 w-4 border-2 border-blue-500 border-t-transparent rounded-full mr-2"></div>
          Searching...
        </div>
      </div>
      
      <!-- No Results -->
      <div v-else-if="!loading && suggestions.length === 0 && searchQuery.length >= 2" class="px-4 py-3 text-gray-500 text-center">
        No suggestions found
      </div>
      
      <!-- Suggestions List -->
      <div v-else>
        <div 
          v-for="(suggestion, index) in suggestions" 
          :key="index"
          @mousedown="selectSuggestion(suggestion)"
          :class="[
            'px-4 py-3 cursor-pointer border-b border-gray-100 last:border-b-0 hover:bg-gray-50 transition',
            { 'bg-blue-50': index === selectedIndex }
          ]"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <!-- Icon based on suggestion type -->
              <div class="mr-3">
                <svg v-if="suggestion.type === 'product'" class="h-4 w-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
                </svg>
                <svg v-else-if="suggestion.type === 'brand'" class="h-4 w-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
                </svg>
                <svg v-else-if="suggestion.type === 'category'" class="h-4 w-4 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                </svg>
              </div>
              
              <!-- Suggestion Text -->
              <div>
                <div class="font-medium text-gray-900">{{ suggestion.text }}</div>
                <div v-if="suggestion.category || suggestion.brand" class="text-xs text-gray-500">
                  <span v-if="suggestion.category">{{ suggestion.category }}</span>
                  <span v-if="suggestion.category && suggestion.brand"> • </span>
                  <span v-if="suggestion.brand">{{ suggestion.brand }}</span>
                </div>
              </div>
            </div>
            
            <!-- Type Badge -->
            <span :class="[
              'px-2 py-1 text-xs rounded-full',
              suggestion.type === 'product' ? 'bg-blue-100 text-blue-800' :
              suggestion.type === 'brand' ? 'bg-green-100 text-green-800' :
              'bg-purple-100 text-purple-800'
            ]">
              {{ suggestion.type }}
            </span>
          </div>
        </div>
        
        <!-- Search Action -->
        <div 
          v-if="searchQuery.length >= 2"
          @mousedown="executeSearch"
          class="px-4 py-3 cursor-pointer border-t border-gray-200 bg-gray-50 hover:bg-gray-100 transition"
        >
          <div class="flex items-center text-blue-600 font-medium">
            <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
            Search for "{{ searchQuery }}"
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'search', 'suggestion-selected'])

// Reactive data
const searchInput = ref(null)
const searchQuery = ref(props.modelValue)
const suggestions = ref([])
const showSuggestions = ref(false)
const loading = ref(false)
const selectedIndex = ref(-1)

// Debounce timer
let suggestionTimeout = null

// Watch for external changes to modelValue
watch(() => props.modelValue, (newValue) => {
  searchQuery.value = newValue
})

// Watch for changes to searchQuery
watch(searchQuery, (newValue) => {
  emit('update:modelValue', newValue)
})

const fetchSuggestions = async (query) => {
  if (query.length < 2) {
    suggestions.value = []
    return
  }
  
  loading.value = true
  
  try {
    const response = await fetch(`http://localhost:8000/api/marketplace/search-suggestions/?q=${encodeURIComponent(query)}`)
    const data = await response.json()
    suggestions.value = data.suggestions || []
  } catch (error) {
    console.error('Error fetching suggestions:', error)
    suggestions.value = []
  } finally {
    loading.value = false
  }
}

const handleInput = () => {
  selectedIndex.value = -1
  
  // Clear previous timeout
  clearTimeout(suggestionTimeout)
  
  // Set new timeout for suggestions
  suggestionTimeout = setTimeout(() => {
    fetchSuggestions(searchQuery.value)
  }, 300) // 300ms delay for suggestions
}

const handleKeydown = (event) => {
  if (!showSuggestions.value || suggestions.value.length === 0) {
    if (event.key === 'Enter') {
      executeSearch()
    }
    return
  }
  
  switch (event.key) {
    case 'ArrowDown':
      event.preventDefault()
      selectedIndex.value = Math.min(selectedIndex.value + 1, suggestions.value.length - 1)
      break
      
    case 'ArrowUp':
      event.preventDefault()
      selectedIndex.value = Math.max(selectedIndex.value - 1, -1)
      break
      
    case 'Enter':
      event.preventDefault()
      if (selectedIndex.value >= 0 && selectedIndex.value < suggestions.value.length) {
        selectSuggestion(suggestions.value[selectedIndex.value])
      } else {
        executeSearch()
      }
      break
      
    case 'Escape':
      showSuggestions.value = false
      selectedIndex.value = -1
      searchInput.value?.blur()
      break
  }
}

const handleBlur = () => {
  // Delay hiding suggestions to allow for click events
  setTimeout(() => {
    showSuggestions.value = false
    selectedIndex.value = -1
  }, 150)
}

const selectSuggestion = (suggestion) => {
  showSuggestions.value = false
  selectedIndex.value = -1
  
  // Emit suggestion selected event to parent
  emit('suggestion-selected', suggestion)
}

const executeSearch = () => {
  showSuggestions.value = false
  selectedIndex.value = -1
  emit('search', searchQuery.value)
}

// Clear suggestions when component unmounts
const clearSuggestions = () => {
  clearTimeout(suggestionTimeout)
  suggestions.value = []
}

// Expose methods for parent component
defineExpose({
  focus: () => searchInput.value?.focus(),
  blur: () => searchInput.value?.blur(),
  clear: () => {
    searchQuery.value = ''
    suggestions.value = []
  }
})
</script>

<style scoped>
/* Custom scrollbar for suggestions */
.max-h-96::-webkit-scrollbar {
  width: 6px;
}

.max-h-96::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.max-h-96::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.max-h-96::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
