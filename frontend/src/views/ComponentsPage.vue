<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">PC Components</h1>
      <p class="text-gray-600">Browse and compare PC components from various vendors</p>
    </div>
    
    <!-- Filters Section -->
    <div class="bg-white rounded-lg shadow-md p-4 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
          <select 
            v-model="filters.category" 
            class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
          >
            <option value="">All Categories</option>
            <option v-for="category in categories" :key="category.slug" :value="category.slug">
              {{ category.name }}
            </option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Manufacturer</label>
          <select 
            v-model="filters.manufacturer" 
            class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
          >
            <option value="">All Manufacturers</option>
            <option v-for="manufacturer in manufacturers" :key="manufacturer.slug" :value="manufacturer.slug">
              {{ manufacturer.name }}
            </option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Sort By</label>
          <select 
            v-model="filters.sortBy" 
            class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
          >
            <option value="name">Name</option>
            <option value="-release_date">Newest First</option>
            <option value="release_date">Oldest First</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Search</label>
          <input 
            v-model="filters.search" 
            type="text" 
            placeholder="Search components..." 
            class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
          >
        </div>
      </div>
      
      <div class="mt-4 flex justify-between items-center">
        <button 
          @click="fetchComponents" 
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
        >
          Apply Filters
        </button>
        
        <button 
          v-if="compareList.length > 0" 
          @click="goToCompare" 
          class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition"
        >
          Compare ({{ compareList.length }})
        </button>
      </div>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-700"></div>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-6">
      <strong class="font-bold">Error!</strong>
      <span class="block sm:inline"> {{ error }}</span>
    </div>
    
    <!-- Empty State -->
    <div v-else-if="components.length === 0" class="text-center py-12">
      <p class="text-gray-500 text-lg">No components found matching your criteria.</p>
      <button 
        @click="resetFilters" 
        class="mt-4 px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition"
      >
        Reset Filters
      </button>
    </div>
    
    <!-- Components Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <ComponentCard 
        v-for="component in components" 
        :key="component.id" 
        :component="component"
        @view-details="viewComponentDetails"
        @add-to-compare="addToCompare"
      />
    </div>
    
    <!-- Pagination -->
    <div v-if="components.length > 0" class="mt-8 flex justify-center">
      <div class="flex space-x-2">
        <button 
          :disabled="!hasPreviousPage" 
          @click="previousPage" 
          class="px-4 py-2 rounded-md border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Previous
        </button>
        <button 
          :disabled="!hasNextPage" 
          @click="nextPage" 
          class="px-4 py-2 rounded-md border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import ComponentCard from '@/components/ComponentCard.vue';

const router = useRouter();

// State
const components = ref([]);
const categories = ref([]);
const manufacturers = ref([]);
const loading = ref(true);
const error = ref(null);
const compareList = ref([]);
const currentPage = ref(1);
const hasNextPage = ref(false);
const hasPreviousPage = ref(false);

// Filters
const filters = reactive({
  category: '',
  manufacturer: '',
  search: '',
  sortBy: 'name',
});

// Fetch components with filters
const fetchComponents = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    let url = '/api/components/components/';
    const params = new URLSearchParams();
    
    if (filters.category) params.append('category__slug', filters.category);
    if (filters.manufacturer) params.append('manufacturer__slug', filters.manufacturer);
    if (filters.search) params.append('search', filters.search);
    if (filters.sortBy) params.append('ordering', filters.sortBy);
    
    // Add page parameter
    params.append('page', currentPage.value);
    
    const response = await axios.get(url, { params });
    components.value = response.data.results || response.data;
    
    // Handle pagination if available
    if (response.data.next) hasNextPage.value = true;
    else hasNextPage.value = false;
    
    if (response.data.previous) hasPreviousPage.value = true;
    else hasPreviousPage.value = false;
    
  } catch (err) {
    console.error('Error fetching components:', err);
    error.value = 'Failed to load components. Please try again.';
  } finally {
    loading.value = false;
  }
};

// Fetch categories and manufacturers for filters
const fetchFilterOptions = async () => {
  try {
    const [categoriesResponse, manufacturersResponse] = await Promise.all([
      axios.get('/api/components/categories/'),
      axios.get('/api/components/manufacturers/')
    ]);
    
    categories.value = categoriesResponse.data.results || categoriesResponse.data;
    manufacturers.value = manufacturersResponse.data.results || manufacturersResponse.data;
  } catch (err) {
    console.error('Error fetching filter options:', err);
  }
};

// Reset all filters
const resetFilters = () => {
  filters.category = '';
  filters.manufacturer = '';
  filters.search = '';
  filters.sortBy = 'name';
  currentPage.value = 1;
  fetchComponents();
};

// Pagination methods
const nextPage = () => {
  if (hasNextPage.value) {
    currentPage.value++;
    fetchComponents();
    window.scrollTo(0, 0);
  }
};

const previousPage = () => {
  if (hasPreviousPage.value) {
    currentPage.value--;
    fetchComponents();
    window.scrollTo(0, 0);
  }
};

// Component actions
const viewComponentDetails = (component) => {
  router.push(`/components/${component.slug}`);
};

const addToCompare = (component) => {
  // Check if component is already in compare list
  const exists = compareList.value.some(item => item.id === component.id);
  
  if (!exists) {
    // Limit to 4 components for comparison
    if (compareList.value.length < 4) {
      compareList.value.push(component);
    } else {
      alert('You can compare up to 4 components at a time.');
    }
  } else {
    // Remove from compare list if already added
    compareList.value = compareList.value.filter(item => item.id !== component.id);
  }
};

const goToCompare = () => {
  if (compareList.value.length > 1) {
    const slugs = compareList.value.map(component => component.slug);
    router.push({
      path: '/compare',
      query: { components: slugs }
    });
  } else {
    alert('Please select at least 2 components to compare.');
  }
};

// Initialize
onMounted(() => {
  fetchFilterOptions();
  fetchComponents();
});
</script>