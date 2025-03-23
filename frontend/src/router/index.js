import { createRouter, createWebHistory } from 'vue-router';
import { authStore } from '@/store';
import commonRoutes from './commonRoutes';
import authRoutes from './authRoutes';
import adminRoutes from './adminRoutes';
import userRoutes from './userRoutes';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [...commonRoutes, ...authRoutes, ...adminRoutes, ...userRoutes],
});

router.beforeEach((to, from, next) => {
  // If at root and logged in, redirect based on role
  if (to.path === '/' && authStore.isLoggedIn) {
    if (authStore.role === 'admin') {
      return next('/admin/home');
    } else if (authStore.role === 'user') {
      return next('/user/home');
    }
  }
  // Admin route guard
  if (to.path.startsWith('/admin') && (!authStore.isLoggedIn || authStore.role !== 'admin')) {
    return next('/login');
  }
  // User route guard
  if (to.path.startsWith('/user') && (!authStore.isLoggedIn || authStore.role !== 'user')) {
    return next('/login');
  }
  next();
});

export default router;
