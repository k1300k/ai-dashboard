import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue')
  },
  {
    path: '/boards',
    name: 'boards',
    component: () => import('@/views/BoardsView.vue')
  },
  {
    path: '/board/:id',
    name: 'board',
    component: () => import('@/views/BoardView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
