<template>
  <div class="min-h-screen bg-gray-50 py-10 px-6 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-8 text-center text-gray-800">Sell Your Product</h1>

    <!-- Select Product Type -->
    <div class="mb-6">
      <label class="block font-semibold mb-2">Select Product Type:</label>
      <select v-model="productType" class="w-full px-4 py-2 border rounded-md shadow-sm">
        <option value="">-- Select --</option>
        <option value="monitor">Monitor</option>
        <option value="ram">RAM</option>
      </select>
    </div>

    <!-- Upload Image -->
    <div class="mb-6">
      <label class="block font-semibold mb-2">Upload Image:</label>
      <input type="file" @change="handleImageUpload" accept="image/*" class="w-full" />
      <div v-if="imagePreview" class="mt-4">
        <img :src="imagePreview" alt="Preview" class="max-w-sm rounded shadow" />
      </div>
    </div>

    <!-- Monitor Form -->
    <div v-if="productType === 'monitor'" class="grid grid-cols-1 gap-4">
      <input v-model="form.brand" type="text" placeholder="Brand" class="input" />
      <input v-model="form.screenSize" type="text" placeholder="Screen Size (e.g., 24 inch)" class="input" />
      <input v-model="form.refreshRate" type="text" placeholder="Refresh Rate (e.g., 144Hz)" class="input" />
      <input v-model="form.panelType" type="text" placeholder="Panel Type (e.g., IPS, VA)" class="input" />
    </div>

    <!-- RAM Form -->
    <div v-if="productType === 'ram'" class="grid grid-cols-1 gap-4">
      <input v-model="form.brand" type="text" placeholder="Brand" class="input" />
      <input v-model="form.name" type="text" placeholder="Model Name" class="input" />
      <input v-model="form.capacity" type="text" placeholder="Capacity (e.g., 8GB, 16GB)" class="input" />
      <select v-model="form.ddrType" class="input">
        <option value="">Select DDR Type</option>
        <option value="DDR3">DDR3</option>
        <option value="DDR4">DDR4</option>
        <option value="DDR5">DDR5</option>
      </select>
    </div>

    <!-- Submit Button -->
    <div class="mt-8 text-center">
      <button @click="submitForm" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold shadow">
        Submit Product
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const productType = ref('')
const imagePreview = ref(null)
const form = ref({
  brand: '',
  screenSize: '',
  refreshRate: '',
  panelType: '',
  name: '',
  capacity: '',
  ddrType: '',
})

function handleImageUpload(e) {
  const file = e.target.files[0]
  if (file) {
    imagePreview.value = URL.createObjectURL(file)
  }
}

function submitForm() {
  console.log('Submitting:', {
    type: productType.value,
    image: imagePreview.value,
    ...form.value
  })
  alert('Product submitted!')
  // Here you would typically send form data to the backend
}
</script>

<style scoped>
.input {
  @apply px-4 py-2 border rounded-md shadow-sm w-full;
}
</style>
