<template>
  <div class="modal-overlay" @click="handleOverlayClick">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>Add New Product</h2>
        <button @click="$emit('close')" class="close-btn">&times;</button>
      </div>
      
      <form @submit.prevent="handleSubmit" class="product-form">
        <div class="form-group">
          <label for="name">Product Name *</label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            required
            placeholder="Enter product name"
          />
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="category">Category *</label>
            <select id="category" v-model="form.category" required>
              <option value="">Select Category</option>
              <option value="CPU">CPU</option>
              <option value="RAM">RAM</option>
              <option value="Storage">Storage</option>
              <option value="Monitor">Monitor</option>
              <option value="Motherboard">Motherboard</option>
              <option value="PSU">PSU</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="condition">Condition *</label>
            <select id="condition" v-model="form.condition" required>
              <option value="">Select Condition</option>
              <option value="Used-Like New">Used-Like New</option>
              <option value="Used-Good">Used-Good</option>
              <option value="Used-Fair">Used-Fair</option>
            </select>
          </div>
        </div>
        
        <div class="form-group">
          <label for="price">Price (৳) *</label>
          <input
            id="price"
            v-model="form.price"
            type="number"
            min="0"
            step="0.01"
            required
            placeholder="Enter price in BDT"
          />
        </div>
        
        <div class="form-group">
          <label for="description">Description *</label>
          <textarea
            id="description"
            v-model="form.description"
            required
            rows="4"
            placeholder="Describe your product..."
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="image">Product Image</label>
          <input
            id="image"
            type="file"
            accept="image/*"
            @change="handleImageChange"
          />
          <div v-if="imagePreview" class="image-preview">
            <img :src="imagePreview" alt="Preview" />
          </div>
        </div>
        
        <div class="form-actions">
          <button type="button" @click="$emit('close')" class="cancel-btn">
            Cancel
          </button>
          <button type="submit" :disabled="loading" class="submit-btn">
            {{ loading ? 'Adding...' : 'Add Product' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'

export default {
  name: 'AddProductModal',
  emits: ['close', 'product-added'],
  setup(props, { emit }) {
    const loading = ref(false)
    const imagePreview = ref(null)
    const selectedImage = ref(null)
    
    const form = reactive({
      name: '',
      category: '',
      condition: '',
      price: '',
      description: '',
    })
    
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
        formData.append('price', form.price)
        formData.append('description', form.description)
        
        if (selectedImage.value) {
          formData.append('image', selectedImage.value)
        }
        
        const token = localStorage.getItem('access_token')
        const response = await fetch('http://localhost:8000/api/marketplace/products/create/', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          },
          body: formData
        })
        
        if (response.ok) {
          emit('product-added')
        } else {
          const errorData = await response.json()
          console.error('Error adding product:', errorData)
          alert('Error adding product. Please try again.')
        }
      } catch (error) {
        console.error('Error adding product:', error)
        alert('Error adding product. Please try again.')
      } finally {
        loading.value = false
      }
    }
    
    const handleOverlayClick = () => {
      emit('close')
    }
    
    return {
      form,
      loading,
      imagePreview,
      handleImageChange,
      handleSubmit,
      handleOverlayClick
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #333;
}

.product-form {
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-row {
  display: flex;
  gap: 15px;
}

.form-row .form-group {
  flex: 1;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
  color: #333;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007bff;
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.image-preview {
  margin-top: 10px;
}

.image-preview img {
  max-width: 200px;
  max-height: 200px;
  border-radius: 6px;
  object-fit: cover;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.cancel-btn,
.submit-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.cancel-btn {
  background: #6c757d;
  color: white;
}

.cancel-btn:hover {
  background: #5a6268;
}

.submit-btn {
  background: #28a745;
  color: white;
}

.submit-btn:hover:not(:disabled) {
  background: #218838;
}

.submit-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    margin: 10px;
  }
  
  .form-row {
    flex-direction: column;
    gap: 0;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>
