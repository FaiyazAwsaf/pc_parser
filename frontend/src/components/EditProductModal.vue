<template>
  <div class="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50" @click="handleOverlayClick">
    <div class="bg-white rounded-lg w-full max-w-4xl max-h-[90vh] overflow-y-auto m-4" @click.stop>
      <div class="flex justify-between items-center p-6 border-b border-gray-200">
        <h2 class="text-2xl font-bold text-gray-800">Edit Product</h2>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 text-2xl font-bold w-8 h-8 flex items-center justify-center">
          &times;
        </button>
      </div>
      
      <form @submit.prevent="handleSubmit" class="p-6 space-y-6">
        <div>
          <label for="name" class="block text-sm font-medium text-gray-700 mb-2">Product Name *</label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            required
            placeholder="Enter product name"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="category" class="block text-sm font-medium text-gray-700 mb-2">Category *</label>
            <select id="category" v-model="form.category" required class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
              <option value="">Select Category</option>
              <option value="CPU">CPU</option>
              <option value="RAM">RAM</option>
              <option value="Storage">Storage</option>
              <option value="Monitor">Monitor</option>
              <option value="Motherboard">Motherboard</option>
              <option value="PSU">PSU</option>
            </select>
          </div>
          
          <div>
            <label for="condition" class="block text-sm font-medium text-gray-700 mb-2">Condition *</label>
            <select id="condition" v-model="form.condition" required class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
              <option value="">Select Condition</option>
              <option value="Used-Like New">Used-Like New</option>
              <option value="Used-Good">Used-Good</option>
              <option value="Used-Fair">Used-Fair</option>
            </select>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="age" class="block text-sm font-medium text-gray-700 mb-2">Age/Usage *</label>
            <select id="age" v-model="form.age" required class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
              <option value="">Select Age</option>
              <option value="0-6months">Less than 6 months</option>
              <option value="6-12months">6-12 months</option>
              <option value="1-2years">1-2 years</option>
              <option value="2plus">2+ years</option>
            </select>
          </div>
          
          <div>
            <label for="warranty" class="block text-sm font-medium text-gray-700 mb-2">Warranty *</label>
            <select id="warranty" v-model="form.warranty" required class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
              <option value="">Select Warranty</option>
              <option value="under">Under warranty</option>
              <option value="expired">Warranty expired</option>
              <option value="none">No warranty info</option>
            </select>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="brand" class="block text-sm font-medium text-gray-700 mb-2">Brand *</label>
            <select id="brand" v-model="form.brand" required class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
              <option value="">Select Brand</option>
              <option value="intel">Intel</option>
              <option value="amd">AMD</option>
              <option value="nvidia">NVIDIA</option>
              <option value="asus">ASUS</option>
              <option value="msi">MSI</option>
              <option value="corsair">Corsair</option>
              <option value="gigabyte">Gigabyte</option>
              <option value="evga">EVGA</option>
              <option value="samsung">Samsung</option>
              <option value="western-digital">Western Digital</option>
            </select>
          </div>
          
          <div>
            <label for="performance_tier" class="block text-sm font-medium text-gray-700 mb-2">Performance Tier *</label>
            <select id="performance_tier" v-model="form.performance_tier" required class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
              <option value="">Select Tier</option>
              <option value="entry">Entry level</option>
              <option value="mid">Mid-range</option>
              <option value="high">High-end</option>
            </select>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="box_accessories" class="block text-sm font-medium text-gray-700 mb-2">Box & Accessories *</label>
            <select id="box_accessories" v-model="form.box_accessories" required class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
              <option value="">Select Status</option>
              <option value="box">Has original box</option>
              <option value="accessories">Has all accessories</option>
              <option value="missing">Missing items</option>
            </select>
          </div>
          
          <div>
            <label for="price_type" class="block text-sm font-medium text-gray-700 mb-2">Price Type *</label>
            <select id="price_type" v-model="form.price_type" required class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
              <option value="">Select Type</option>
              <option value="fixed">Fixed price</option>
              <option value="negotiable">Price negotiable</option>
            </select>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="availability" class="block text-sm font-medium text-gray-700 mb-2">Availability *</label>
            <select id="availability" v-model="form.availability" required class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
              <option value="">Select Availability</option>
              <option value="now">Available now</option>
              <option value="soon">Available soon</option>
            </select>
          </div>
          
          <div>
            <label for="compatibility" class="block text-sm font-medium text-gray-700 mb-2">Compatibility</label>
            <select id="compatibility" v-model="form.compatibility" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
              <option value="">Select Compatibility (Optional)</option>
              <option value="lga1700">LGA1700</option>
              <option value="am4">AM4</option>
              <option value="am5">AM5</option>
              <option value="ddr4">DDR4</option>
              <option value="ddr5">DDR5</option>
              <option value="atx">ATX</option>
              <option value="micro-atx">Micro-ATX</option>
              <option value="mini-itx">Mini-ITX</option>
            </select>
          </div>
        </div>
        
        <div>
          <label for="price" class="block text-sm font-medium text-gray-700 mb-2">Price (৳) *</label>
          <input
            id="price"
            v-model="form.price"
            type="number"
            min="0"
            step="0.01"
            required
            placeholder="Enter price in BDT"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        
        <div>
          <label for="description" class="block text-sm font-medium text-gray-700 mb-2">Description *</label>
          <textarea
            id="description"
            v-model="form.description"
            required
            rows="4"
            placeholder="Describe your product..."
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-vertical"
          ></textarea>
        </div>
        
        <div>
          <label for="image" class="block text-sm font-medium text-gray-700 mb-2">Product Image</label>
          <input
            id="image"
            type="file"
            accept="image/*"
            @change="handleImageChange"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
          <div v-if="imagePreview" class="mt-3">
            <img :src="imagePreview" alt="Preview" class="max-w-48 max-h-48 rounded-md object-cover" />
          </div>
        </div>
        
        <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200">
          <button 
            type="button" 
            @click="$emit('close')" 
            class="px-6 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 transition"
          >
            Cancel
          </button>
          <button 
            type="submit" 
            :disabled="loading" 
            class="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
          >
            {{ loading ? 'Updating...' : 'Update Product' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'product-updated'])

const loading = ref(false)
const imagePreview = ref(null)
const selectedImage = ref(null)

const form = reactive({
  name: '',
  category: '',
  condition: '',
  age: '',
  warranty: '',
  brand: '',
  performance_tier: '',
  box_accessories: '',
  price_type: 'fixed',
  availability: 'now',
  compatibility: '',
  price: '',
  description: '',
})

watch(() => props.product, (newProduct) => {
  if (newProduct) {
    Object.keys(form).forEach(key => {
      form[key] = newProduct[key] || ''
    })
    if (newProduct.image) {
      imagePreview.value = newProduct.image
    }
  }
}, { immediate: true })

const handleImageChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedImage.value = file
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const handleSubmit = async () => {
  loading.value = true
  
  try {
    const formData = new FormData()
    formData.append('name', form.name)
    formData.append('category', form.category)
    formData.append('condition', form.condition)
    formData.append('age', form.age)
    formData.append('warranty', form.warranty)
    formData.append('brand', form.brand)
    formData.append('performance_tier', form.performance_tier)
    formData.append('box_accessories', form.box_accessories)
    formData.append('price_type', form.price_type)
    formData.append('availability', form.availability)
    formData.append('compatibility', form.compatibility)
    formData.append('price', form.price)
    formData.append('description', form.description)
    
    if (selectedImage.value) {
      formData.append('image', selectedImage.value)
    }
    
    const token = localStorage.getItem('access_token')
    const response = await fetch(`http://localhost:8000/api/marketplace/products/my/${props.product.id}/`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    })
    
    if (response.ok) {
      emit('product-updated')
    } else {
      const errorData = await response.json()
      console.error('Error updating product:', errorData)
      alert('Error updating product. Please try again.')
    }
  } catch (error) {
    console.error('Error updating product:', error)
    alert('Error updating product. Please try again.')
  } finally {
    loading.value = false
  }
}

const handleOverlayClick = () => {
  emit('close')
}
</script>
