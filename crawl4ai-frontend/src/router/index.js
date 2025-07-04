import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Dashboard from '../views/Dashboard.vue'
import CrawlFilter from '../views/dashboard/CrawlFilter.vue'
import DataShowcase from '../views/dashboard/DataShowcase.vue'
import TaskManager from '../views/dashboard/TaskManager.vue'
import TaskResults from '../views/dashboard/TaskResults.vue'
import CreateTask from "@/views/dashboard/CreateTask.vue"
import CrawlTemplate from '@/views/dashboard/CrawlTemplate.vue'
import User from '../views/dashboard/User.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/dashboard', component: Dashboard },
  {
    path: '/dashboard',
    component: Dashboard,
    children: [
      { path: '', redirect: 'home' }, // 默认跳转到 dashboard/home
      { path: 'crawlFilter', component: CrawlFilter },
      { path: 'dataShowcase', component: DataShowcase },
      { path: 'task', component: TaskManager },
      { path: 'task/:id/results', component: TaskResults },
      { path: 'createTask', component: CreateTask },
      { path: 'case',component: CrawlTemplate },
      { path: 'user',component: User },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
