export default [
  {
    path: '/admin',
    component: () => import('../views/admin/AdminLayout.vue'),
    children: [
      {
        path: '',
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
        component: () => import('../views/admin/forms/AdminSubjectForm.vue'),
      },
      {
        path: 'edit-subject/:id',
        component: () => import('../views/admin/forms/AdminSubjectForm.vue'),
      },
      {
        path: 'new-chapter/:subject_id',
        component: () => import('../views/admin/forms/AdminChapterForm.vue'),
      },
      {
        path: 'edit-chapter/:id',
        component: () => import('../views/admin/forms/AdminChapterForm.vue'),
      },
      {
        path: 'new-quiz',
        component: () => import('../views/admin/forms/AdminQuizForm.vue'),
      },
      {
        path: 'edit-quiz/:id',
        component: () => import('../views/admin/forms/AdminQuizForm.vue'),
      },
      {
        path: 'new-question/:quiz_id',
        component: () => import('../views/admin/forms/AdminQuestionForm.vue'),
      },
      {
        path: 'edit-question/:id',
        component: () => import('../views/admin/forms/AdminQuestionForm.vue'),
      },
    ],
  },
];
