<template>
  <div class="min-h-screen bg-white">
    <!-- Gradient Banner -->
    <div class="bg-gradient-to-br from-slate-900 to-blue-800 text-white py-10 px-6 text-center">
      <h1 class="text-3xl md:text-4xl font-extrabold">Choose A CPU</h1>
    </div>

    <div class="p-6 grid grid-cols-1 lg:grid-cols-5 gap-6">
      <!-- Sidebar Filters -->
      <aside class="lg:col-span-1 space-y-6">
        <!-- Price Filter -->
        <div v-if="filterOptions.price_range">
          <label class="font-semibold block mb-1">Price</label>
          <input
            type="range"
            :min="filterOptions.price_range.min_price || 0"
            :max="filterOptions.price_range.max_price || 5000"
            v-model="filters.maxPrice"
            class="w-full"
          />
          <div class="text-sm text-gray-600">Tk. {{ filters.maxPrice }}</div>
        </div>

        <!-- Manufacturer Filter -->
        <div v-if="filterOptions.manufacturers && filterOptions.manufacturers.length">
          <label class="font-semibold block mb-1">Manufacturer</label>
          <div class="space-y-1">
            <label
              v-for="manufacturer in filterOptions.manufacturers"
              :key="manufacturer"
              class="flex items-center gap-2"
            >
              <input
                type="checkbox"
                v-model="filters.selectedManufacturers"
                :value="manufacturer"
              />
              {{ manufacturer }}
            </label>
          </div>
        </div>

        <!-- Core Count Filter -->
        <div
          v-if="
            filterOptions.specs &&
            filterOptions.specs.core_counts &&
            filterOptions.specs.core_counts.length
          "
        >
          <label class="font-semibold block mb-1">Core Count</label>
          <div class="space-y-1">
            <label
              v-for="cores in filterOptions.specs.core_counts"
              :key="cores"
              class="flex items-center gap-2"
            >
              <input type="checkbox" v-model="filters.selectedCoreCounts" :value="cores" />
              {{ cores }} Cores
            </label>
          </div>
        </div>

        <!-- Base Frequency Filter -->
        <div
          v-if="
            filterOptions.specs &&
            filterOptions.specs.base_frequencies &&
            filterOptions.specs.base_frequencies.length
          "
        >
          <label class="font-semibold block mb-1">Base Frequency</label>
          <div class="space-y-1">
            <label
              v-for="freq in filterOptions.specs.base_frequencies.slice(0, 10)"
              :key="freq"
              class="flex items-center gap-2"
            >
              <input type="checkbox" v-model="filters.selectedBaseFreqs" :value="freq" />
              {{ freq }} GHz
            </label>
          </div>
        </div>

        <!-- Cache Filter -->
        <div
          v-if="
            filterOptions.specs &&
            filterOptions.specs.cache_sizes &&
            filterOptions.specs.cache_sizes.length
          "
        >
          <label class="font-semibold block mb-1">Cache</label>
          <div class="space-y-1">
            <label
              v-for="cache in filterOptions.specs.cache_sizes.slice(0, 10)"
              :key="cache"
              class="flex items-center gap-2"
            >
              <input type="checkbox" v-model="filters.selectedCacheSizes" :value="cache" />
              {{ cache }} MB
            </label>
          </div>
        </div>

        <!-- Integrated Graphics Filter -->
        <div
          v-if="
            filterOptions.specs &&
            filterOptions.specs.graphics_options &&
            filterOptions.specs.graphics_options.length
          "
        >
          <label class="font-semibold block mb-1">Integrated Graphics</label>
          <div class="space-y-1">
            <label
              v-for="graphics in filterOptions.specs.graphics_options.slice(0, 8)"
              :key="graphics"
              class="flex items-center gap-2"
            >
              <input type="checkbox" v-model="filters.selectedGraphics" :value="graphics" />
              {{ graphics }}
            </label>
          </div>
        </div>
      </aside>

      <!-- Main Content Table -->
      <main class="lg:col-span-4">
        <div v-if="loading" class="text-center py-8">
          <div
            class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"
          ></div>
          <p class="mt-2 text-gray-600">Loading CPUs...</p>
        </div>

        <div v-else-if="error" class="text-center py-8">
          <p class="text-red-600">{{ error }}</p>
          <button @click="fetchData" class="mt-2 bg-blue-600 text-white px-4 py-2 rounded">
            Retry
          </button>
        </div>

        <!-- CPUs Table -->
        <div v-else class="overflow-x-auto">
          <table class="w-full table-auto border-collapse">
            <thead class="bg-gray-100">
              <tr>
                <th></th>
                <th class="text-left px-3 py-2">Name</th>
                <th class="text-left px-3 py-2">Brand</th>
                <th class="text-left px-3 py-2">Model</th>
                <th class="text-left px-3 py-2">Core Count</th>
                <th class="text-left px-3 py-2">Base Clock</th>
                <th class="text-left px-3 py-2">Boost Clock</th>
                <th class="text-left px-3 py-2">Cache</th>
                <th class="text-left px-3 py-2">Graphics</th>
                <th class="text-left px-3 py-2">Price</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="cpu in filteredCpus" :key="cpu.id" class="border-b hover:bg-gray-50">
                <td class="px-2 py-3"><input type="checkbox" /></td>
                <td class="px-3 py-2">{{ cpu.name }}</td>
                <td class="px-3 py-2">{{ cpu.brand || 'N/A' }}</td>
                <td class="px-3 py-2">{{ cpu.model || 'N/A' }}</td>
                <td class="px-3 py-2">{{ getSpecValue(cpu.specs, 'core_count') || 'N/A' }}</td>
                <td class="px-3 py-2">{{ getSpecValue(cpu.specs, 'base_clock') || 'N/A' }}</td>
                <td class="px-3 py-2">{{ getSpecValue(cpu.specs, 'boost_clock') || 'N/A' }}</td>
                <td class="px-3 py-2">{{ getSpecValue(cpu.specs, 'l3_cache') || 'N/A' }}</td>
                <td class="px-3 py-2">{{ getSpecValue(cpu.specs, 'graphics') || 'None' }}</td>
                <td class="px-3 py-2">
                  <span v-if="cpu.lowest_price" class="text-green-600 font-semibold">
                    Tk. {{ cpu.lowest_price }}
                  </span>
                  <span v-else class="text-gray-400">No price</span>
                </td>
                <td class="px-3 py-2">
                  <button
                    @click="viewDetails(cpu)"
                    class="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
                  >
                    Details
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- No Results -->
          <div v-if="filteredCpus.length === 0" class="text-center py-8">
            <p class="text-gray-600">No CPUs found matching your criteria.</p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Data
const cpus = ref([])
const filterOptions = ref({})
const loading = ref(true)
const error = ref(null)
const searchQuery = ref('')

// Filters
const filters = ref({
  maxPrice: 5000,
  selectedManufacturers: [],
  selectedCoreCounts: [],
  selectedBaseFreqs: [],
  selectedCacheSizes: [],
  selectedGraphics: [],
})

// Computed filtered CPUs
const filteredCpus = computed(() => {
  let filtered = cpus.value.filter((cpu) => {
    // Search filter
    if (searchQuery.value) {
      const search = searchQuery.value.toLowerCase()
      if (
        !cpu.name.toLowerCase().includes(search) &&
        !cpu.brand?.toLowerCase().includes(search) &&
        !cpu.model?.toLowerCase().includes(search)
      ) {
        return false
      }
    }

    // Price filter
    if (cpu.lowest_price && cpu.lowest_price > filters.value.maxPrice) {
      return false
    }

    // Manufacturer filter
    if (
      filters.value.selectedManufacturers.length > 0 &&
      !filters.value.selectedManufacturers.includes(cpu.brand)
    ) {
      return false
    }

    // Core count filter
    if (filters.value.selectedCoreCounts.length > 0) {
      const coreCount = parseInt(getSpecValue(cpu.specs, 'core_count'))
      if (!coreCount || !filters.value.selectedCoreCounts.includes(coreCount)) {
        return false
      }
    }

    // Base frequency filter
    if (filters.value.selectedBaseFreqs.length > 0) {
      const baseFreq = parseFloat(getSpecValue(cpu.specs, 'base_clock')?.replace('GHz', ''))
      if (!baseFreq || !filters.value.selectedBaseFreqs.some((f) => Math.abs(f - baseFreq) < 0.1)) {
        return false
      }
    }

    // Cache filter
    if (filters.value.selectedCacheSizes.length > 0) {
      const cache = parseFloat(getSpecValue(cpu.specs, 'l3_cache')?.replace('MB', ''))
      if (!cache || !filters.value.selectedCacheSizes.includes(cache)) {
        return false
      }
    }

    // Graphics filter
    if (filters.value.selectedGraphics.length > 0) {
      const graphics = getSpecValue(cpu.specs, 'graphics')
      if (!graphics || !filters.value.selectedGraphics.includes(graphics)) {
        return false
      }
    }

    return true
  })

  return filtered
})

// Helper function to get spec values
const getSpecValue = (specs, key) => {
  return specs && specs[key] ? specs[key] : null
}

// Fetch data from API
const fetchData = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await fetch('http://localhost:8000/api/components/category/CPU/')

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    cpus.value = data.results || []
    filterOptions.value = data.filters || {}

    // Set initial max price from API data
    if (filterOptions.value.price_range?.max_price) {
      filters.value.maxPrice = filterOptions.value.price_range.max_price
    }
  } catch (err) {
    error.value = `Failed to load CPUs: ${err.message}`
    console.error('Error fetching CPUs:', err)
  } finally {
    loading.value = false
  }
}

// View CPU details
const viewDetails = (cpu) => {
  // Navigate to component detail page
  router.push(`/components/${cpu.id}`)
}

// Watch for filter changes and refetch data
watch(
  [searchQuery, filters],
  async () => {
    // You could implement debounced API calls with filters here
    // For now, we'll filter on the frontend
  },
  { deep: true },
)

// Fetch data on component mount
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
th,
td {
  font-size: 0.95rem;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
