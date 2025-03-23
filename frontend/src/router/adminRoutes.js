export default [
  {
    path: '/admin',
    component: () => import('../views/admin/AdminLayout.vue'),
    children: [
      // Main admin pages
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

      // Subject management routes
      {
        path: 'subject/new',
        component: () => import('../views/admin/forms/AdminSubjectForm.vue'),
      },
      {
        path: 'subject/:id/edit',
        component: () => import('../views/admin/forms/AdminSubjectForm.vue'),
      },

      // Chapter management routes
      {
        path: 'subject/:subject_id/chapter/new',
        component: () => import('../views/admin/forms/AdminChapterForm.vue'),
      },
      {
        path: 'chapter/:id/edit',
        component: () => import('../views/admin/forms/AdminChapterForm.vue'),
      },

      // Quiz management routes
      {
        path: 'quiz/new',
        component: () => import('../views/admin/forms/AdminQuizForm.vue'),
      },
      {
        path: 'quiz/:id/edit',
        component: () => import('../views/admin/forms/AdminQuizForm.vue'),
      },

      // Question management routes
      {
        path: 'quiz/:quiz_id/question/new',
        component: () => import('../views/admin/forms/AdminQuestionForm.vue'),
      },
      {
        path: 'question/:id/edit',
        component: () => import('../views/admin/forms/AdminQuestionForm.vue'),
      },
    ],
  },
];
