import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '@/views/LandingPage.vue'
import ComponentsPage from '@/views/ComponentsPage.vue'
import ComponentDetailPage from '@/views/ComponentDetailPage.vue'
import LoginPage from '@/views/LoginPage.vue'
import RegisterPage from '@/views/RegisterPage.vue'
import EmailVerificationPage from '@/views/EmailVerificationPage.vue'
import MarketplacePage from '@/views/MarketplacePage.vue'

const routes = [
  { path: '/', component: LandingPage },
  { path: '/components', component: ComponentsPage },
  { path: '/components/:slug', component: ComponentDetailPage },
  { path: '/marketplace', component: MarketplacePage },
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage },
  { path: '/verify-email', component: EmailVerificationPage },
  // Route for component comparison will be added later
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
