import { createRouter, createWebHistory } from 'vue-router';
import store from '@/store';

const commonRoutes = [
  {
    path: '/',
    component: () => import('../views/common/CommonHome.vue'),
  },
  {
    // catch-all route using parameter with custom regexp
    // https://router.vuejs.org/guide/migration/#Removed-star-or-catch-all-routes
    path: '/:pathMatch(.*)*',
    component: () => import('../views/common/CommonNotFound.vue'),
  },
];

const authRoutes = [
  {
    path: '/login',
    component: () => import('../views/auth/Login.vue'),
  },
  {
    path: '/register',
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
        component: () => import('../views/admin/AdminHome.vue'),
      },
      {
        path: 'home',
        component: () => import('../views/admin/AdminHome.vue'),
      },
      {
        path: 'quizzes',
        component: () => import('../views/admin/AdminQuizzes.vue'),
      },
      {
        path: 'users',
        component: () => import('../views/admin/AdminUsers.vue'),
      },
      {
        path: 'summary',
        component: () => import('../views/admin/AdminSummary.vue'),
      },
      {
        path: 'new-subject',
        component: () => import('../views/admin/AdminNewSubject.vue'),
      },
      {
        path: 'edit-subject/:id',
        component: () => import('../views/admin/AdminEditSubject.vue'),
      },
      {
        path: 'new-chapter/:subject_id',
        component: () => import('../views/admin/AdminNewChapter.vue'),
      },
      {
        path: 'edit-chapter/:id',
        component: () => import('../views/admin/AdminEditChapter.vue'),
      },
      {
        path: 'new-quiz/:chapter_id',
        component: () => import('../views/admin/AdminNewQuiz.vue'),
      },
      {
        path: 'edit-quiz/:id',
        component: () => import('../views/admin/AdminEditQuiz.vue'),
      },
      {
        path: 'new-question/:quiz_id',
        component: () => import('../views/admin/AdminNewQuestion.vue'),
      },
      {
        path: 'edit-question/:id',
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
        component: () => import('../views/user/UserHome.vue'),
      },
      {
        path: 'home',
        component: () => import('../views/user/UserHome.vue'),
      },
      {
        path: 'view-quiz/:subject_id',
        component: () => import('../views/user/UserViewQuiz.vue'),
      },
      {
        path: 'do-quiz/:quiz_id',
        component: () => import('../views/user/UserDoQuiz.vue'),
      },
      {
        path: 'scores',
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
