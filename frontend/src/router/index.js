import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '@/views/LandingPage.vue'
import ComponentsPage from '@/views/ComponentsPage.vue'
import ComponentDetailPage from '@/views/ComponentDetailPage.vue'

const routes = [
  { path: '/', component: LandingPage },
  { path: '/components', component: ComponentsPage },
  { path: '/components/:slug', component: ComponentDetailPage },
  // Route for component comparison will be added later
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
