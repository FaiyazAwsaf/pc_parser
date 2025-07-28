<template>
  <div class="component-card bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
    <div class="relative">
      <img 
        :src="component.image || '/placeholder-component.png'" 
        :alt="component.name"
        class="w-full h-48 object-contain bg-gray-100 p-4"
      />
      <span 
        v-if="component.lowest_price && component.lowest_price.is_on_sale" 
        class="absolute top-2 right-2 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full"
      >
        On Sale
      </span>
    </div>
    
    <div class="p-4">
      <div class="flex items-center justify-between mb-2">
        <span class="text-xs text-gray-500">{{ component.category.name }}</span>
        <span class="text-xs font-medium text-blue-600">{{ component.manufacturer.name }}</span>
      </div>
      
      <h3 class="text-lg font-semibold text-gray-800 mb-1 truncate">{{ component.name }}</h3>
      <p class="text-sm text-gray-600 mb-3 truncate">{{ component.model_number }}</p>
      
      <div v-if="component.lowest_price" class="flex justify-between items-end">
        <div>
          <p class="text-sm text-gray-500">Lowest Price:</p>
          <p class="text-xl font-bold text-blue-700">
            {{ component.lowest_price.price }} {{ component.lowest_price.currency }}
          </p>
          <p class="text-xs text-gray-500">{{ component.lowest_price.vendor_name }}</p>
        </div>
        
        <div class="flex space-x-2">
          <button 
            @click="$emit('view-details', component)" 
            class="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 transition"
          >
            Details
          </button>
          <button 
            @click="$emit('add-to-compare', component)" 
            class="px-3 py-1 bg-gray-200 text-gray-700 text-sm rounded hover:bg-gray-300 transition"
          >
            Compare
          </button>
        </div>
      </div>
      
      <div v-else class="text-center py-2">
        <p class="text-gray-500 text-sm">No price information available</p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  component: {
    type: Object,
    required: true
  }
});

defineEmits(['view-details', 'add-to-compare']);
</script>