<template>
  <div class="min-h-screen bg-white">
    <!-- Gradient Header -->
    <div class="bg-gradient-to-br from-slate-900 to-blue-800 text-white py-10 text-center">
      <h1 class="text-3xl md:text-4xl font-extrabold">Choose A Monitor</h1>
    </div>

    <div class="max-w-7xl mx-auto px-4 py-10 grid grid-cols-1 md:grid-cols-4 gap-10">
      <!-- Filters -->
      <aside class="space-y-6">
        <div>
          <h2 class="font-semibold mb-2">PRICE</h2>
          <input type="range" min="50" max="3000" v-model="filters.price" class="w-full" />
          <p class="text-sm">Up to ${{ filters.price }}</p>
        </div>

        <div>
          <h2 class="font-semibold mb-2">MANUFACTURER</h2>
          <div class="space-y-1">
            <div v-for="brand in brandOptions" :key="brand">
              <input type="checkbox" :id="brand" v-model="filters.manufacturer" :value="brand" />
              <label :for="brand" class="ml-2">{{ brand }}</label>
            </div>
          </div>
        </div>

        <div>
          <h2 class="font-semibold mb-2">RATING</h2>
          <div class="space-y-1">
            <div v-for="star in [5,4,3,2,1]" :key="star">
              <input type="checkbox" :id="'star-' + star" v-model="filters.rating" :value="star" />
              <label :for="'star-' + star" class="ml-2">{{ star }} stars & up</label>
            </div>
          </div>
        </div>

        <div>
          <h2 class="font-semibold mb-2">PANEL TYPE</h2>
          <select v-model="filters.panelType" class="w-full p-2 border rounded">
            <option value="">All</option>
            <option value="IPS">IPS</option>
            <option value="TN">TN</option>
            <option value="VA">VA</option>
          </select>
        </div>

        <div>
          <h2 class="font-semibold mb-2">REFRESH RATE</h2>
          <input type="range" min="60" max="240" v-model="filters.refreshRate" class="w-full" />
          <p class="text-sm">{{ filters.refreshRate }} Hz</p>
        </div>
      </aside>

      <!-- Table -->
      <section class="md:col-span-3 overflow-x-auto">
        <div class="flex justify-between mb-4 items-center">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search Monitor"
            class="border p-2 rounded w-full max-w-md"
          />
          <button class="ml-4 px-4 py-2 bg-blue-600 text-white rounded">Add From Selection</button>
        </div>

        <table class="min-w-full border border-gray-300 text-sm">
          <thead class="bg-gray-100">
            <tr>
              <th class="px-4 py-2 text-left">NAME</th>
              <th class="px-4 py-2 text-left">SCREEN SIZE</th>
              <th class="px-4 py-2 text-left">RESOLUTION</th>
              <th class="px-4 py-2 text-left">REFRESH RATE</th>
              <th class="px-4 py-2 text-left">PANEL TYPE</th>
              <th class="px-4 py-2 text-left">RESPONSE TIME</th>
              <th class="px-4 py-2 text-left">ASPECT RATIO</th>
              <th class="px-4 py-2 text-left">RATING</th>
              <th class="px-4 py-2 text-left">PRICE</th>
              <th class="px-4 py-2 text-left"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="monitor in filteredMonitors" :key="monitor.name" class="border-t">
              <td class="px-4 py-2">{{ monitor.name }}</td>
              <td class="px-4 py-2">{{ monitor.screenSize }}"</td>
              <td class="px-4 py-2">{{ monitor.resolution }}</td>
              <td class="px-4 py-2">{{ monitor.refreshRate }}Hz</td>
              <td class="px-4 py-2">{{ monitor.panelType }}</td>
              <td class="px-4 py-2">{{ monitor.responseTime }}ms</td>
              <td class="px-4 py-2">{{ monitor.aspectRatio }}</td>
              <td class="px-4 py-2">{{ monitor.rating }} ⭐</td>
              <td class="px-4 py-2">${{ monitor.price }}</td>
              <td class="px-4 py-2">
                <button class="bg-blue-600 text-white px-3 py-1 rounded">Add</button>
              </td>
            </tr>
          </tbody>
        </table>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const searchQuery = ref('')
const filters = ref({
  price: 1000,
  manufacturer: [],
  rating: [],
  panelType: '',
  refreshRate: 144
})

const brandOptions = ['Samsung', 'LG', 'Acer', 'Asus', 'Dell']

const monitorList = ref([
  {
    name: 'LG UltraGear 27GN750-B',
    screenSize: 27,
    resolution: '1920x1080',
    refreshRate: 240,
    panelType: 'IPS',
    responseTime: 1,
    aspectRatio: '16:9',
    rating: 5,
    manufacturer: 'LG',
    price: 329
  },
  {
    name: 'Samsung Odyssey G7',
    screenSize: 32,
    resolution: '2560x1440',
    refreshRate: 240,
    panelType: 'VA',
    responseTime: 1,
    aspectRatio: '16:9',
    rating: 4,
    manufacturer: 'Samsung',
    price: 599
  }
  // Add more as needed
])

const filteredMonitors = computed(() => {
  return monitorList.value.filter(m => {
    return (
      (!filters.value.manufacturer.length || filters.value.manufacturer.includes(m.manufacturer)) &&
      (!filters.value.rating.length || filters.value.rating.some(r => m.rating >= r)) &&
      (!filters.value.panelType || filters.value.panelType === m.panelType) &&
      m.price <= filters.value.price &&
      m.refreshRate >= filters.value.refreshRate &&
      m.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  })
})
</script>
