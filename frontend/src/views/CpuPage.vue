<template>
  <div class="min-h-screen bg-white">
    <!-- Gradient Banner -->
    <div class="bg-gradient-to-br from-slate-900 to-blue-800 text-white py-10 px-6 text-center">
      <h1 class="text-3xl md:text-4xl font-extrabold">Choose A CPU</h1>
    </div>

    <div class="p-6 grid grid-cols-1 lg:grid-cols-5 gap-6">
      <!-- Sidebar Filters -->
      <aside class="lg:col-span-1 space-y-6">
        <div>
          <label class="font-semibold block mb-1">Price</label>
          <input type="range" min="0" max="2600" v-model="filters.price" class="w-full">
          <div class="text-sm text-gray-600">${{ filters.price }}</div>
        </div>

        <div>
          <label class="font-semibold block mb-1">Manufacturer</label>
          <div class="space-y-1">
            <label v-for="maker in ['All', 'AMD', 'Intel']" :key="maker" class="flex items-center gap-2">
              <input type="checkbox" v-model="filters.manufacturer" :value="maker">
              {{ maker }}
            </label>
          </div>
        </div>

        <div>
          <label class="font-semibold block mb-1">Rating</label>
          <div class="space-y-1">
            <label v-for="star in [5, 4, 3, 2, 1, 0]" :key="star" class="flex items-center gap-2">
              <input type="checkbox" v-model="filters.rating" :value="star">
              {{ star === 0 ? 'Unrated' : `${star}★` }}
            </label>
          </div>
        </div>

        <div>
          <label class="font-semibold block mb-1">Core Count</label>
          <input type="range" min="1" max="64" v-model="filters.coreCount" class="w-full">
          <div class="text-sm text-gray-600">{{ filters.coreCount }} Cores</div>
        </div>

        <div>
          <label class="font-semibold block mb-1">Base Frequency</label>
          <input type="range" min="1.1" max="4.7" step="0.1" v-model="filters.baseFreq" class="w-full">
          <div class="text-sm text-gray-600">{{ filters.baseFreq }} GHz</div>
        </div>

        <div>
          <label class="font-semibold block mb-1">Max Frequency</label>
          <input type="range" min="1.1" max="5.5" step="0.1" v-model="filters.maxFreq" class="w-full">
          <div class="text-sm text-gray-600">{{ filters.maxFreq }} GHz</div>
        </div>

        <div>
          <label class="font-semibold block mb-1">Cache</label>
          <input type="range" min="0" max="256" v-model="filters.cache" class="w-full">
          <div class="text-sm text-gray-600">{{ filters.cache }} MB</div>
        </div>

        <div>
          <label class="font-semibold block mb-1">Integrated Graphics</label>
          <div class="space-y-1">
            <label v-for="option in ['All', 'None', 'Intel UHD Graphics 630', 'Intel UHD Graphics 770', 'Intel Xe', 'Radeon']" :key="option" class="flex items-center gap-2">
              <input type="checkbox" v-model="filters.graphics" :value="option">
              {{ option }}
            </label>
          </div>
        </div>
      </aside>

      <!-- Main Content Table -->
      <main class="lg:col-span-4">
        <div class="flex justify-between items-center mb-4">
          <input type="text" placeholder="Search CPU" v-model="search" class="border rounded px-4 py-2 w-full max-w-sm">
          <button class="ml-4 bg-blue-600 text-white px-4 py-2 rounded">Add From Selection</button>
        </div>

        <table class="w-full table-auto border-collapse">
          <thead class="bg-gray-100">
            <tr>
              <th></th>
              <th class="text-left px-3 py-2">Name</th>
              <th class="text-left px-3 py-2">Core Count</th>
              <th class="text-left px-3 py-2">Base Freq</th>
              <th class="text-left px-3 py-2">Max Freq</th>
              <th class="text-left px-3 py-2">Cache</th>
              <th class="text-left px-3 py-2">Graphics</th>
              <th class="text-left px-3 py-2">Rating</th>
              <th class="text-left px-3 py-2">Price</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="cpu in filteredCpus" :key="cpu.name" class="border-b hover:bg-gray-50">
              <td class="px-2 py-3"><input type="checkbox"></td>
              <td class="px-3 py-2">{{ cpu.name }}</td>
              <td class="px-3 py-2">{{ cpu.cores }}</td>
              <td class="px-3 py-2">{{ cpu.base }} GHz</td>
              <td class="px-3 py-2">{{ cpu.max }} GHz</td>
              <td class="px-3 py-2">{{ cpu.cache }} MB</td>
              <td class="px-3 py-2">{{ cpu.graphics }}</td>
              <td class="px-3 py-2">{{ cpu.rating }}★</td>
              <td class="px-3 py-2">${{ cpu.price }}</td>
              <td class="px-3 py-2"><button class="bg-blue-500 text-white px-3 py-1 rounded">Add</button></td>
            </tr>
          </tbody>
        </table>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const search = ref('')
const filters = ref({
  price: 2600,
  manufacturer: [],
  rating: [],
  coreCount: 64,
  baseFreq: 4.7,
  maxFreq: 5.5,
  cache: 256,
  graphics: []
})

const cpuList = ref([
  {
    name: 'AMD Ryzen 7 5800X3D', cores: 8, base: 3.4, max: 4.5, cache: 96, graphics: 'None', rating: 5, price: 329
  },
  {
    name: 'Intel Core i7-12700K', cores: 12, base: 3.6, max: 5.0, cache: 25, graphics: 'Intel UHD Graphics 770', rating: 4, price: 419
  },
  {
    name: 'AMD Ryzen 5 7600X', cores: 6, base: 4.7, max: 5.3, cache: 32, graphics: 'Radeon', rating: 4, price: 279
  }
])

const filteredCpus = computed(() => {
  return cpuList.value.filter(cpu => {
    return cpu.name.toLowerCase().includes(search.value.toLowerCase())
  })
})
</script>

<style scoped>
th, td {
  font-size: 0.95rem;
}
</style>
