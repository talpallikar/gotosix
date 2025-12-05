import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store'

import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Scenarios from '../views/Scenarios.vue'
import ScenarioDetail from '../views/ScenarioDetail.vue'
import Decklists from '../views/Decklists.vue'
import DecklistDetail from '../views/DecklistDetail.vue'
import CreateDecklist from '../views/CreateDecklist.vue'
import CreateScenario from '../views/CreateScenario.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/scenarios', name: 'Scenarios', component: Scenarios },
  { path: '/scenarios/:id', name: 'ScenarioDetail', component: ScenarioDetail },
  { path: '/decklists', name: 'Decklists', component: Decklists },
  { path: '/decklists/:id', name: 'DecklistDetail', component: DecklistDetail },
  {
    path: '/decklists/new',
    name: 'CreateDecklist',
    component: CreateDecklist,
    meta: { requiresAuth: true }
  },
  {
    path: '/scenarios/new',
    name: 'CreateScenario',
    component: CreateScenario,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router
