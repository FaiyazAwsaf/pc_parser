import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '@/views/LandingPage.vue'

const routes = [
  { path: '/', component: LandingPage },
  // ...other routes
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
