export default [
  {
    path: '/',
    component: () => import('../views/common/CommonHome.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    component: () => import('../views/common/CommonNotFound.vue'),
  },
];
