<template>
  <div class="min-h-screen bg-white">
    <!-- Gradient Header -->
    <div class="bg-gradient-to-br from-slate-900 to-blue-800 text-white py-10 text-center rounded-b-xl shadow">
      <h1 class="text-3xl md:text-4xl font-extrabold">PC Parts Marketplace</h1>
    </div>

    <div class="max-w-7xl mx-auto px-4 py-10 grid grid-cols-1 md:grid-cols-4 gap-10">
      <!-- Sidebar Filters -->
      <aside class="space-y-6">
        <div>
          <h2 class="font-semibold mb-2">FILTER</h2>
        </div>
        <div>
          <h2 class="font-semibold mb-2">CATEGORY</h2>
          <select v-model="filters.category" class="w-full p-2 border rounded">
            <option value="">All Categories</option>
            <option v-for="cat in categoryOptions" :key="cat" :value="cat">{{ cat }}</option>
          </select>
        </div>
        <div>
          <h2 class="font-semibold mb-2">CONDITION</h2>
          <select v-model="filters.condition" class="w-full p-2 border rounded">
            <option value="">All Conditions</option>
            <option v-for="cond in conditionOptions" :key="cond" :value="cond">{{ cond }}</option>
          </select>
        </div>
        <div>
          <h2 class="font-semibold mb-2">PRICE RANGE (৳)</h2>
          <input type="range" min="0" max="100000" step="1000" v-model="filters.price" class="w-full" />
          <p class="text-sm">Up to ৳{{ formatPrice(filters.price) }}</p>
        </div>
        <div>
          <button @click="goToSellPage" class="w-full px-3 py-3 bg-orange-500 text-white border-none rounded-lg cursor-pointer text-base hover:bg-orange-600 transition-colors font-bold">
            Sell a Product
          </button>
        </div>
      </aside>

      <!-- Product Grid & Search -->
      <section class="md:col-span-3 overflow-x-auto">
        <div class="flex flex-col md:flex-row md:justify-between mb-6 items-center gap-4">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search for products..."
            class="border p-2 rounded w-full md:max-w-md"
          />
        </div>
        <div>
          <table class="min-w-full border border-gray-300 text-sm">
            <thead class="bg-gray-100">
              <tr>
                <th class="px-4 py-2 text-left">NAME</th>
                <th class="px-4 py-2 text-left">CATEGORY</th>
                <th class="px-4 py-2 text-left">CONDITION</th>
                <th class="px-4 py-2 text-left">PRICE</th>
                <th class="px-4 py-2 text-left"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="product in filteredProducts" :key="product.name" class="border-t">
                <td class="px-4 py-2">{{ product.name }}</td>
                <td class="px-4 py-2">{{ product.category }}</td>
                <td class="px-4 py-2">{{ product.condition }}</td>
                <td class="px-4 py-2">৳{{ formatPrice(product.price) }}</td>
                <td class="px-4 py-2">
                  <button class="bg-blue-600 text-white px-3 py-1 rounded">Order</button>
                </td>
              </tr>
              <tr v-if="filteredProducts.length === 0">
                <td colspan="5" class="text-center py-8 text-gray-500">No products found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const searchQuery = ref('')
const filters = ref({
  category: '',
  condition: '',
  price: 100000
})

const categoryOptions = ['CPU', 'GPU', 'RAM', 'Motherboard', 'SSD', 'HDD', 'Monitor', 'Keyboard', 'Mouse']
const conditionOptions = ['New', 'Used', 'Refurbished']

const productList = ref([
  { name: 'AMD Ryzen 5 5600X', category: 'CPU', condition: 'New', price: 16500 },
  { name: 'Samsung 980 Pro SSD', category: 'SSD', condition: 'New', price: 8000 },
  { name: 'Corsair Vengeance 16GB', category: 'RAM', condition: 'Used', price: 4000 },
  { name: 'Asus RTX 3070', category: 'GPU', condition: 'Used', price: 57000 },
  { name: 'A4Tech Mouse', category: 'Mouse', condition: 'New', price: 900 },
  // Add more as needed
])

const filteredProducts = computed(() => {
  return productList.value.filter(p => {
    return (
      (!filters.value.category || p.category === filters.value.category) &&
      (!filters.value.condition || p.condition === filters.value.condition) &&
      p.price <= filters.value.price &&
      p.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  })
})

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-BD').format(price)
}

const goToSellPage = () => {
  router.push('/sell')
}
</script>
