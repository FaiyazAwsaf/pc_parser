import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '@/views/LandingPage.vue'
import ComponentsPage from '@/views/ComponentsPage.vue'
import ComponentDetailPage from '@/views/ComponentDetailPage.vue'
import MarketplacePage from '@/views/MarketplacePage.vue'

const routes = [
  { path: '/', component: LandingPage },
  { path: '/components', component: ComponentsPage },
  { path: '/components/:slug', component: ComponentDetailPage },
  { path: '/marketplace', component: MarketplacePage },
  // Route for component comparison will be added later
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
