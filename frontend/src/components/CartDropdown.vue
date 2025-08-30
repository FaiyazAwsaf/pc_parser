<template>
  <div class="relative">
    <button
      @click="toggleCart"
      class="relative p-2 text-gray-600 hover:text-blue-600 transition-colors"
    >
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-1.5 6M7 13l-1.5 6m0 0h9M17 13v6a2 2 0 01-2 2H9a2 2 0 01-2-2v-6"></path>
      </svg>
      <span
        v-if="cartCount > 0"
        class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center"
      >
        {{ cartCount }}
      </span>
    </button>

    <div
      v-if="isCartOpen"
      class="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg z-50 border border-gray-200"
    >
      <div class="p-4">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-gray-800">Shopping Cart</h3>
          <button
            @click="closeCart"
            class="text-gray-400 hover:text-gray-600"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <div v-if="cartItems.length === 0" class="text-center py-8">
          <div class="text-4xl mb-2">🛒</div>
          <p class="text-gray-500">Your cart is empty</p>
        </div>

        <div v-else>
          <div class="max-h-64 overflow-y-auto">
            <div
              v-for="item in cartItems"
              :key="item.id"
              class="flex items-center space-x-3 py-3 border-b border-gray-100 last:border-b-0"
            >
              <img
                :src="item.image || '/placeholder-product.jpg'"
                :alt="item.name"
                class="w-12 h-12 object-cover rounded"
              />
              <div class="flex-1 min-w-0">
                <h4 class="text-sm font-medium text-gray-900 truncate">{{ item.name }}</h4>
                <p class="text-sm text-gray-500">৳{{ formatPrice(item.price) }}</p>
              </div>
              <div class="flex items-center space-x-2">
                <button
                  @click="updateQuantity(item.id, item.quantity - 1)"
                  class="w-6 h-6 rounded-full bg-gray-200 flex items-center justify-center text-gray-600 hover:bg-gray-300"
                >
                  -
                </button>
                <span class="text-sm font-medium w-8 text-center">{{ item.quantity }}</span>
                <button
                  @click="updateQuantity(item.id, item.quantity + 1)"
                  class="w-6 h-6 rounded-full bg-gray-200 flex items-center justify-center text-gray-600 hover:bg-gray-300"
                >
                  +
                </button>
                <button
                  @click="removeFromCart(item.id)"
                  class="text-red-500 hover:text-red-700 ml-2"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <div class="mt-4 pt-4 border-t border-gray-200">
            <div class="flex justify-between items-center mb-4">
              <span class="text-lg font-semibold text-gray-900">Total:</span>
              <span class="text-lg font-bold text-blue-600">৳{{ formatPrice(cartTotal) }}</span>
            </div>
            <div class="space-y-2">
              <button
                @click="proceedToCheckout"
                class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition"
              >
                Proceed to Checkout
              </button>
              <button
                @click="clearCart"
                class="w-full bg-gray-200 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-300 transition"
              >
                Clear Cart
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCart } from '../stores/cart.js'

const {
  cartItems,
  isCartOpen,
  cartCount,
  cartTotal,
  addToCart,
  removeFromCart,
  updateQuantity,
  clearCart,
  toggleCart,
  closeCart
} = useCart()

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-BD').format(price)
}

const proceedToCheckout = async () => {
  if (cartItems.value.length === 0) return

  try {
    const token = localStorage.getItem('access_token')
    const orders = []
    const totalAmount = cartTotal.value

    for (const item of cartItems.value) {
      const orderData = {
        product: item.id,
        quantity: item.quantity,
        shipping_address: 'Default Address',
        status: 'delivered'
      }

      const response = await fetch('http://localhost:8000/api/marketplace/orders/create/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(orderData)
      })

      if (response.ok) {
        const order = await response.json()
        orders.push(order)
      } else {
        const errorText = await response.text()
        console.error('Order creation failed:', errorText)
        throw new Error(`Failed to create order for ${item.name}`)
      }
    }

    clearCart()
    closeCart()

    alert(`Successfully placed ${orders.length} order(s)! Total: ৳${formatPrice(totalAmount)}`)

    window.dispatchEvent(new CustomEvent('orderPlaced', { detail: orders }))

  } catch (error) {
    console.error('Error placing orders:', error)
    alert('Error placing orders. Please try again.')
  }
}
</script>
