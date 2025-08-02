<template>
  <div class="min-h-screen bg-white">
    <!-- Gradient Header -->
    <div class="bg-gradient-to-br from-slate-900 to-blue-800 text-white py-10 text-center">
      <h1 class="text-3xl md:text-4xl font-extrabold">Choose A Memory</h1>
    </div>

    <div class="max-w-7xl mx-auto px-4 py-10 grid grid-cols-1 md:grid-cols-4 gap-10">
      <!-- Filters -->
      <aside class="space-y-6">
        <div>
          <h2 class="font-semibold mb-2">PRICE</h2>
          <input type="range" min="20" max="500" v-model="filters.price" class="w-full" />
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
          <h2 class="font-semibold mb-2">MEMORY TYPE</h2>
          <select v-model="filters.type" class="w-full p-2 border rounded">
            <option value="">All</option>
            <option value="DDR3">DDR3</option>
            <option value="DDR4">DDR4</option>
            <option value="DDR5">DDR5</option>
          </select>
        </div>

        <div>
          <h2 class="font-semibold mb-2">CAPACITY</h2>
          <select v-model="filters.capacity" class="w-full p-2 border rounded">
            <option value="">All</option>
            <option value="4">4GB</option>
            <option value="8">8GB</option>
            <option value="16">16GB</option>
            <option value="32">32GB</option>
          </select>
        </div>
      </aside>

      <!-- Table -->
      <section class="md:col-span-3 overflow-x-auto">
        <div class="flex justify-between mb-4 items-center">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search Memory"
            class="border p-2 rounded w-full max-w-md"
          />
          <button class="ml-4 px-4 py-2 bg-blue-600 text-white rounded">Add From Selection</button>
        </div>

        <table class="min-w-full border border-gray-300 text-sm">
          <thead class="bg-gray-100">
            <tr>
              <th class="px-4 py-2 text-left">IMAGE</th>
              <th class="px-4 py-2 text-left">NAME</th>
              <th class="px-4 py-2 text-left">TYPE</th>
              <th class="px-4 py-2 text-left">CAPACITY</th>
              <th class="px-4 py-2 text-left">FREQUENCY</th>
              <th class="px-4 py-2 text-left">RATING</th>
              <th class="px-4 py-2 text-left">PRICE</th>
              <th class="px-4 py-2 text-left"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="ram in filteredMemory" :key="ram.name" class="border-t">
              <td class="px-4 py-2"><img :src="ram.image" alt="ram image" class="w-16 h-10 object-contain" /></td>
              <td class="px-4 py-2">{{ ram.name }}</td>
              <td class="px-4 py-2">{{ ram.type }}</td>
              <td class="px-4 py-2">{{ ram.capacity }}GB</td>
              <td class="px-4 py-2">{{ ram.frequency }}MHz</td>
              <td class="px-4 py-2">{{ ram.rating }} ⭐</td>
              <td class="px-4 py-2">${{ ram.price }}</td>
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
  price: 500,
  manufacturer: [],
  rating: [],
  type: '',
  capacity: ''
})

const brandOptions = ['Corsair', 'G.Skill', 'Kingston', 'TeamGroup']

const memoryList = ref([
  {
    name: 'Corsair Vengeance LPX',
    type: 'DDR4',
    capacity: 16,
    frequency: 3200,
    rating: 5,
    manufacturer: 'Corsair',
    price: 89,
    image: 'https://via.placeholder.com/100x40?text=RAM1'
  },
  {
    name: 'G.Skill Ripjaws V',
    type: 'DDR4',
    capacity: 8,
    frequency: 3000,
    rating: 4,
    manufacturer: 'G.Skill',
    price: 45,
    image: 'https://via.placeholder.com/100x40?text=RAM2'
  }
])

const filteredMemory = computed(() => {
  return memoryList.value.filter(m => {
    return (
      (!filters.value.manufacturer.length || filters.value.manufacturer.includes(m.manufacturer)) &&
      (!filters.value.rating.length || filters.value.rating.some(r => m.rating >= r)) &&
      (!filters.value.type || filters.value.type === m.type) &&
      (!filters.value.capacity || parseInt(filters.value.capacity) === m.capacity) &&
      m.price <= filters.value.price &&
      m.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  })
})
</script>
