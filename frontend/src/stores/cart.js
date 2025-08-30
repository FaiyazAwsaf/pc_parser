import { ref, computed } from 'vue'

const cartItems = ref([])
const isCartOpen = ref(false)

export const useCart = () => {
  const addToCart = (product) => {
    const existingItem = cartItems.value.find(item => item.id === product.id)
    
    if (existingItem) {
      existingItem.quantity += 1
    } else {
      cartItems.value.push({
        ...product,
        quantity: 1
      })
    }
  }

  const removeFromCart = (productId) => {
    const index = cartItems.value.findIndex(item => item.id === productId)
    if (index > -1) {
      cartItems.value.splice(index, 1)
    }
  }

  const updateQuantity = (productId, quantity) => {
    const item = cartItems.value.find(item => item.id === productId)
    if (item) {
      if (quantity <= 0) {
        removeFromCart(productId)
      } else {
        item.quantity = quantity
      }
    }
  }

  const clearCart = () => {
    cartItems.value = []
  }

  const toggleCart = () => {
    isCartOpen.value = !isCartOpen.value
  }

  const openCart = () => {
    isCartOpen.value = true
  }

  const closeCart = () => {
    isCartOpen.value = false
  }

  const cartCount = computed(() => {
    return cartItems.value.reduce((total, item) => total + item.quantity, 0)
  })

  const cartTotal = computed(() => {
    return cartItems.value.reduce((total, item) => total + (item.price * item.quantity), 0)
  })

  const isInCart = (productId) => {
    return cartItems.value.some(item => item.id === productId)
  }

  const getCartItemQuantity = (productId) => {
    const item = cartItems.value.find(item => item.id === productId)
    return item ? item.quantity : 0
  }

  return {
    cartItems: computed(() => cartItems.value),
    isCartOpen: computed(() => isCartOpen.value),
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
    toggleCart,
    openCart,
    closeCart,
    cartCount,
    cartTotal,
    isInCart,
    getCartItemQuantity
  }
}
