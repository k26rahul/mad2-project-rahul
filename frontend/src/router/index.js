import { createRouter, createWebHistory } from 'vue-router';
import store from '@/store';
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
  if (to.path === '/' && store.auth.isLoggedIn) {
    if (store.auth.role === 'admin') {
      return next('/admin/home');
    } else if (store.auth.role === 'user') {
      return next('/user/home');
    }
  }
  // Admin route guard
  if (to.path.startsWith('/admin') && (!store.auth.isLoggedIn || store.auth.role !== 'admin')) {
    return next('/login');
  }
  // User route guard
  if (to.path.startsWith('/user') && (!store.auth.isLoggedIn || store.auth.role !== 'user')) {
    return next('/login');
  }
  next();
});

export default router;
