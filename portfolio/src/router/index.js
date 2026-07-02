import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/admin',
    redirect: '/admin/login'
  },
  {
    path: '/admin/login',
    name: 'Login',
    component: () => import('../views/admin/Login.vue')
  },
  {
    path: '/admin/profile-cms',
    name: 'ProfileCMS',
    component: () => import('../views/admin/ProfileCMS.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/users',
    name: 'Users',
    component: () => import('../views/admin/Users.vue'),
    meta: { requiresAuth: true, requiresSuperAdmin: true }
  },
  {
    path: '/admin/users/create',
    name: 'UserCreate',
    component: () => import('../views/admin/UserForm.vue'),
    meta: { requiresAuth: true, requiresSuperAdmin: true }
  },
  {
    path: '/admin/users/:id/edit',
    name: 'UserEdit',
    component: () => import('../views/admin/UserForm.vue'),
    meta: { requiresAuth: true, requiresSuperAdmin: true }
  },
  {
    path: '/admin/profile',
    name: 'Profile',
    component: () => import('../views/admin/Profile.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    }
    return { top: 0 }
  }
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('auth_token')
  const userType = localStorage.getItem('user_type')

  if (to.meta.requiresAuth && !token) {
    next('/admin/login')
  } else if (to.meta.requiresSuperAdmin && userType !== 'SUPERADMIN') {
    next('/admin/profile-cms')
  } else if (to.path === '/admin/login' && token) {
    next('/admin/profile-cms')
  } else {
    next()
  }
})

export default router
