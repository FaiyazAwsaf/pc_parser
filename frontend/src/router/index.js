import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '@/views/LandingPage.vue'
import ComponentsPage from '@/views/ComponentsPage.vue'
import ComponentDetailPage from '@/views/ComponentDetailPage.vue'
import LoginPage from '@/views/LoginPage.vue'
import RegisterPage from '@/views/RegisterPage.vue'
import EmailVerificationPage from '@/views/EmailVerificationPage.vue'
import MarketplacePage from '@/views/MarketplacePage.vue'
import ProfilePage from '@/views/ProfilePage.vue'
import BuildHelperPage from '@/views/BuildHelperPage.vue'
import AboutPage from '@/views/AboutPage.vue' 
import SellComponents from '@/views/SellComponents.vue'
import CpuPage from '@/views/CpuPage.vue'
import MonitorPage from '@/views/MonitorPage.vue'
import MemoryPage from '@/views/MemoryPage.vue'

const routes = [
  { path: '/', component: LandingPage },
  { path: '/components', component: ComponentsPage },
  // Specific component category pages should come BEFORE the generic detail routes
  { path: '/components/cpu', component: CpuPage },
  { path: '/components/monitor', component: MonitorPage },
  { path: '/components/memory', component: MemoryPage },
  // Component detail routes - these should come AFTER specific category routes
  { path: '/components/:id(\\d+)', component: ComponentDetailPage },
  { path: '/components/:slug', component: ComponentDetailPage },
  { path: '/marketplace', component: MarketplacePage },
  { path: '/profile', component: ProfilePage },
  { path: '/builder', component: BuildHelperPage },
  { path: '/about', component: AboutPage },
  { path: '/sell', component: SellComponents },
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage },
  { path: '/verify-email', component: EmailVerificationPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
