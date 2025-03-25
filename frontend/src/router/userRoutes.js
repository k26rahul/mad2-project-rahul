export default [
  {
    path: '/user',
    component: () => import('../views/user/UserLayout.vue'),
    children: [
      {
        path: 'home',
        component: () => import('../views/user/UserHome.vue'),
      },
      {
        path: 'quiz/:quiz_id',
        component: () => import('../views/user/UserViewQuiz.vue'),
      },
      {
        path: 'quiz/:quiz_id/attempt',
        component: () => import('../views/user/UserAttemptQuiz.vue'),
      },
      {
        path: 'scores',
        component: () => import('../views/user/UserScores.vue'),
      },
      {
        path: 'summary',
        component: () => import('../views/user/UserSummary.vue'),
      },
    ],
  },
];
