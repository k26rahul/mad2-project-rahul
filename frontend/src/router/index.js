import { createRouter, createWebHistory } from 'vue-router';
import store from '@/store';

const commonRoutes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/common/CommonHome.vue'),
  },
  {
    // catch-all route using parameter with custom regexp
    // https://router.vuejs.org/guide/migration/#Removed-star-or-catch-all-routes
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/common/CommonNotFound.vue'),
  },
];

const authRoutes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/Login.vue'),
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/auth/Register.vue'),
  },
];

const adminRoutes = [
  {
    path: '/admin',
    component: () => import('../views/admin/AdminLayout.vue'), // Admin layout component
    children: [
      {
        path: '', // Default child route
        name: 'admin.default',
        component: () => import('../views/admin/AdminHome.vue'),
      },
      {
        path: 'home',
        name: 'admin.home',
        component: () => import('../views/admin/AdminHome.vue'),
      },
      {
        path: 'users',
        name: 'admin.users',
        component: () => import('../views/admin/AdminUsers.vue'),
      },
      {
        path: 'new-subject',
        name: 'admin.newSubject',
        component: () => import('../views/admin/AdminNewSubject.vue'),
      },
      {
        path: 'edit-subject/:id',
        name: 'admin.editSubject',
        component: () => import('../views/admin/AdminEditSubject.vue'),
      },
      {
        path: 'new-chapter/:subject_id',
        name: 'admin.newChapter',
        component: () => import('../views/admin/AdminNewChapter.vue'),
      },
      {
        path: 'edit-chapter/:id',
        name: 'admin.editChapter',
        component: () => import('../views/admin/AdminEditChapter.vue'),
      },
      {
        path: 'new-quiz/:chapter_id',
        name: 'admin.newQuiz',
        component: () => import('../views/admin/AdminNewQuiz.vue'),
      },
      {
        path: 'edit-quiz/:id',
        name: 'admin.editQuiz',
        component: () => import('../views/admin/AdminEditQuiz.vue'),
      },
      {
        path: 'new-question/:quiz_id',
        name: 'admin.newQuestion',
        component: () => import('../views/admin/AdminNewQuestion.vue'),
      },
      {
        path: 'edit-question/:id',
        name: 'admin.editQuestion',
        component: () => import('../views/admin/AdminEditQuestion.vue'),
      },
    ],
  },
];

const userRoutes = [
  {
    path: '/user',
    component: () => import('../views/user/UserLayout.vue'), // User layout component
    children: [
      {
        path: '', // Default child route
        name: 'user.default',
        component: () => import('../views/user/UserHome.vue'),
      },
      {
        path: 'home',
        name: 'user.home',
        component: () => import('../views/user/UserHome.vue'),
      },
      {
        path: 'view-quiz/:subject_id',
        name: 'user.viewQuiz',
        component: () => import('../views/user/UserViewQuiz.vue'),
      },
      {
        path: 'do-quiz/:quiz_id',
        name: 'user.doQuiz',
        component: () => import('../views/user/UserDoQuiz.vue'),
      },
      {
        path: 'scores',
        name: 'user.scores',
        component: () => import('../views/user/UserScores.vue'),
      },
    ],
  },
];

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
