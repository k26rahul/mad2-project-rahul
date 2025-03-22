export default [
  {
    path: '/user',
    component: () => import('../views/user/UserLayout.vue'),
    children: [
      {
        path: '',
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
