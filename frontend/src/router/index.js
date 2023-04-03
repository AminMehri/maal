import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'
import UserDashboardView from '../views/UserDashboardView.vue'
import ProfileView from '../views/ProfileView.vue'
import ConfirmEmailView from '../views/ConfirmEmailView.vue'
import ResetPasswordView from '../views/ResetPasswordView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { loginRedirect: true }
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: { loginRedirect: true }
  },
  {
    path: '/dashboard/overview',
    name: 'dashboard',
    component: DashboardView,
    meta: { loginRequired: true }
  },
  {
    path: '/dashboard/:username',
    name: 'user_dashboard',
    component: UserDashboardView,
    meta: { loginRequired: true }
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    meta: { loginRequired: true }
  },
  {
    path: '/confirmEmail/:token/:id',
    name: 'confirm_email',
    component: ConfirmEmailView,
  },
  {
    path: '/resetPassword/:token/:id',
    name: 'reset_password',
    component: ResetPasswordView,
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.loginRequired)) {
    if (store.state.isAuthenticated) {
      next()
    } else {
      next("/")
    }
  }else if (to.matched.some(record => record.meta.loginRedirect)) {
    if (store.state.isAuthenticated) {
      next("/profile")
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router