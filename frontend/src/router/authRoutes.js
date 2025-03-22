export default [
  {
    path: '/login',
    component: () => import('../views/auth/Login.vue'),
  },
  {
    path: '/register',
    component: () => import('../views/auth/Register.vue'),
  },
];
