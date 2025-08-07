<template>
  <div class="flex items-center">
    <!-- Stars -->
    <div class="flex items-center">
      <button
        v-for="star in 5"
        :key="star"
        @click="interactive ? setRating(star) : null"
        @mouseover="interactive ? hoverRating = star : null"
        @mouseleave="interactive ? hoverRating = 0 : null"
        :class="[
          'focus:outline-none transition-colors duration-150',
          interactive ? 'cursor-pointer hover:scale-110 transform' : 'cursor-default',
          star <= (interactive ? (hoverRating || modelValue) : modelValue) 
            ? 'text-yellow-400' 
            : 'text-gray-300'
        ]"
        :disabled="!interactive"
      >
        <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20">
          <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z"/>
        </svg>
      </button>
    </div>
    
    <!-- Rating text -->
    <span v-if="showText" class="ml-2 text-sm text-gray-600">
      <template v-if="modelValue > 0">
        {{ modelValue.toFixed(1) }}
        <span v-if="count !== undefined" class="text-gray-400">
          ({{ count }} {{ count === 1 ? 'review' : 'reviews' }})
        </span>
      </template>
      <span v-else class="text-gray-400">No reviews</span>
    </span>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  modelValue: {
    type: Number,
    default: 0
  },
  interactive: {
    type: Boolean,
    default: false
  },
  showText: {
    type: Boolean,
    default: true
  },
  count: {
    type: Number,
    default: undefined
  }
})

const emit = defineEmits(['update:modelValue'])

const hoverRating = ref(0)

const setRating = (rating) => {
  if (props.interactive) {
    emit('update:modelValue', rating)
  }
}
</script>
