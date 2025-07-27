<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-700"></div>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-6">
      <strong class="font-bold">Error!</strong>
      <span class="block sm:inline"> {{ error }}</span>
      <button @click="router.push('/components')" class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md">
        Back to Components
      </button>
    </div>
    
    <!-- Component Details -->
    <div v-else class="bg-white rounded-lg shadow-lg overflow-hidden">
      <!-- Header -->
      <div class="flex flex-col md:flex-row">
        <!-- Image -->
        <div class="md:w-1/3 p-6 flex items-center justify-center bg-gray-100">
          <img 
            :src="component.image || '/placeholder-component.png'" 
            :alt="component.name"
            class="max-w-full max-h-64 object-contain"
          />
        </div>
        
        <!-- Basic Info -->
        <div class="md:w-2/3 p-6">
          <div class="flex items-center mb-2">
            <span class="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded mr-2">
              {{ component.category?.name }}
            </span>
            <span class="bg-gray-100 text-gray-800 text-xs font-medium px-2.5 py-0.5 rounded">
              {{ component.manufacturer?.name }}
            </span>
          </div>
          
          <h1 class="text-3xl font-bold text-gray-800 mb-2">{{ component.name }}</h1>
          <p class="text-gray-600 mb-4">Model: {{ component.model_number }}</p>
          
          <div v-if="lowestPrice" class="mb-6">
            <p class="text-sm text-gray-500 mb-1">Lowest Price:</p>
            <div class="flex items-baseline">
              <span class="text-3xl font-bold text-blue-700 mr-2">
                {{ lowestPrice.price }} {{ lowestPrice.currency }}
              </span>
              <span class="text-sm text-gray-500">
                at {{ lowestPrice.vendor_name }}
              </span>
            </div>
            <a 
              :href="lowestPrice.vendor_url" 
              target="_blank" 
              class="inline-block mt-2 text-blue-600 hover:underline"
            >
              Visit Store
            </a>
          </div>
          
          <div class="flex space-x-3">
            <button 
              @click="router.push('/components')" 
              class="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50 transition"
            >
              Back to Components
            </button>
            <button 
              @click="addToCompare" 
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
            >
              Add to Compare
            </button>
          </div>
        </div>
      </div>
      
      <!-- Tabs -->
      <div class="border-t border-gray-200">
        <div class="flex border-b">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              'px-4 py-2 text-sm font-medium',
              activeTab === tab.id 
                ? 'border-b-2 border-blue-500 text-blue-600' 
                : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            {{ tab.name }}
          </button>
        </div>
        
        <!-- Specifications Tab -->
        <div v-if="activeTab === 'specs'" class="p-6">
          <h2 class="text-xl font-semibold mb-4">Specifications</h2>
          <div v-if="Object.keys(component.specifications || {}).length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="(value, key) in component.specifications" :key="key" class="border-b pb-2">
              <span class="text-sm text-gray-500">{{ formatSpecKey(key) }}:</span>
              <span class="ml-2 font-medium">{{ value }}</span>
            </div>
          </div>
          <p v-else class="text-gray-500">No specification details available.</p>
          
          <div class="mt-6">
            <h3 class="text-lg font-semibold mb-2">Description</h3>
            <p class="text-gray-700 whitespace-pre-line">{{ component.description || 'No description available.' }}</p>
          </div>
        </div>
        
        <!-- Prices Tab -->
        <div v-if="activeTab === 'prices'" class="p-6">
          <h2 class="text-xl font-semibold mb-4">Available Prices</h2>
          <div v-if="component.prices && component.prices.length > 0" class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Vendor</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Last Updated</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="price in component.prices" :key="price.id">
                  <td class="px-6 py-4 whitespace-nowrap">{{ price.vendor_name }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-baseline">
                      <span class="text-lg font-bold text-gray-900">{{ price.price }} {{ price.currency }}</span>
                      <span 
                        v-if="price.is_on_sale && price.original_price" 
                        class="ml-2 text-sm line-through text-gray-500"
                      >
                        {{ price.original_price }} {{ price.currency }}
                      </span>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span 
                      v-if="price.is_on_sale" 
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800"
                    >
                      On Sale
                    </span>
                    <span 
                      v-else-if="price.is_available" 
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800"
                    >
                      In Stock
                    </span>
                    <span 
                      v-else 
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800"
                    >
                      Out of Stock
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ formatDate(price.last_checked) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm">
                    <a 
                      :href="price.vendor_url" 
                      target="_blank" 
                      class="text-blue-600 hover:text-blue-900 hover:underline"
                    >
                      Visit Store
                    </a>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <p v-else class="text-gray-500">No price information available.</p>
        </div>
        
        <!-- Price History Tab -->
        <div v-if="activeTab === 'history'" class="p-6">
          <h2 class="text-xl font-semibold mb-4">Price History</h2>
          <div v-if="component.price_history && component.price_history.length > 0">
            <p class="text-sm text-gray-500 mb-4">Price trends over the last 30 days</p>
            <!-- Price history chart would go here -->
            <div class="h-64 bg-gray-100 rounded flex items-center justify-center">
              <p class="text-gray-500">Price history chart visualization would be implemented here</p>
            </div>
            
            <div class="mt-6 overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Vendor</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="record in component.price_history" :key="record.id">
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ formatDate(record.recorded_at) }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {{ record.vendor_name }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {{ record.price }} {{ record.currency }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <p v-else class="text-gray-500">No price history available.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const route = useRoute();

// State
const component = ref({});
const loading = ref(true);
const error = ref(null);
const activeTab = ref('specs');

// Tabs configuration
const tabs = [
  { id: 'specs', name: 'Specifications' },
  { id: 'prices', name: 'Available Prices' },
  { id: 'history', name: 'Price History' }
];

// Computed properties
const lowestPrice = computed(() => {
  if (!component.value.prices || component.value.prices.length === 0) return null;
  return [...component.value.prices].sort((a, b) => a.price - b.price)[0];
});

// Methods
const fetchComponentDetails = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const slug = route.params.slug;
    const response = await axios.get(`/api/components/components/${slug}/`);
    component.value = response.data;
  } catch (err) {
    console.error('Error fetching component details:', err);
    error.value = 'Failed to load component details. Please try again.';
  } finally {
    loading.value = false;
  }
};

const addToCompare = () => {
  // This would typically use a store to manage comparison state
  // For now, we'll just navigate to the compare page with this component
  router.push({
    path: '/compare',
    query: { components: [component.value.slug] }
  });
};

const formatDate = (dateString) => {
  if (!dateString) return 'Unknown';
  const date = new Date(dateString);
  return date.toLocaleDateString();
};

const formatSpecKey = (key) => {
  // Convert camelCase or snake_case to Title Case with spaces
  return key
    .replace(/_/g, ' ')
    .replace(/([A-Z])/g, ' $1')
    .replace(/^./, str => str.toUpperCase())
    .trim();
};

// Initialize
onMounted(() => {
  fetchComponentDetails();
});
</script>