import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'cases',
    component: () => import('@/views/CasesView.vue'),
    meta: { title: 'Cases' },
  },
  {
    path: '/cases/:slug',
    name: 'case',
    component: () => import('@/views/CaseDetailView.vue'),
    meta: { title: 'Case' },
  },
  {
    path: '/donations/:reference',
    name: 'donation-success',
    component: () => import('@/views/DonationSuccessView.vue'),
    meta: { title: 'Thank you', auth: true },
  },
  {
    path: '/account',
    name: 'account',
    component: () => import('@/views/AccountView.vue'),
    meta: { title: 'Your account', auth: true },
  },
  {
    path: '/top-up',
    name: 'top-up',
    component: () => import('@/views/TopUpView.vue'),
    meta: { title: 'Top up', auth: true },
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue'),
    meta: { title: 'Log in', guest: true },
  },
  {
    path: '/signup',
    name: 'signup',
    component: () => import('@/views/SignupView.vue'),
    meta: { title: 'Create account', guest: true },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFoundView.vue'),
    meta: { title: 'Not found' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, saved) {
    if (saved) return saved
    if (to.name === from.name && to.name === 'cases') return false
    return { top: 0 }
  },
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  await auth.init()
  if (to.meta.auth && !auth.isAuthenticated) {
    return { name: 'login', query: { next: to.fullPath } }
  }
  if (to.meta.guest && auth.isAuthenticated) {
    return { name: 'cases' }
  }
})

router.afterEach((to) => {
  document.title = to.meta.title ? `${to.meta.title} · Shefa mini` : 'Shefa mini'
})

export default router
