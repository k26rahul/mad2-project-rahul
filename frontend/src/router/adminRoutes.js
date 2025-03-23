export default [
  {
    path: '/admin',
    component: () => import('../views/admin/AdminLayout.vue'),
    children: [
      // Main admin pages
      {
        path: 'home',
        name: 'AdminHome',
        component: () => import('../views/admin/AdminHome.vue'),
      },
      {
        path: 'quizzes',
        name: 'AdminQuizzes',
        component: () => import('../views/admin/AdminQuizzes.vue'),
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('../views/admin/AdminUsers.vue'),
      },
      {
        path: 'summary',
        name: 'AdminSummary',
        component: () => import('../views/admin/AdminSummary.vue'),
      },

      // Subject management routes
      {
        path: 'subject/new',
        name: 'AdminSubjectNew',
        component: () => import('../views/admin/forms/AdminSubjectForm.vue'),
      },
      {
        path: 'subject/:id/edit',
        name: 'AdminSubjectEdit',
        component: () => import('../views/admin/forms/AdminSubjectForm.vue'),
      },

      // Chapter management routes
      {
        path: 'subject/:subject_id/chapter/new',
        name: 'AdminChapterNew',
        component: () => import('../views/admin/forms/AdminChapterForm.vue'),
      },
      {
        path: 'chapter/:id/edit',
        name: 'AdminChapterEdit',
        component: () => import('../views/admin/forms/AdminChapterForm.vue'),
      },

      // Quiz management routes
      {
        path: 'quiz/new',
        name: 'AdminQuizNew',
        component: () => import('../views/admin/forms/AdminQuizForm.vue'),
      },
      {
        path: 'quiz/:id/edit',
        name: 'AdminQuizEdit',
        component: () => import('../views/admin/forms/AdminQuizForm.vue'),
      },

      // Question management routes
      {
        path: 'quiz/:quiz_id/question/new',
        name: 'AdminQuestionNew',
        component: () => import('../views/admin/forms/AdminQuestionForm.vue'),
      },
      {
        path: 'question/:id/edit',
        name: 'AdminQuestionEdit',
        component: () => import('../views/admin/forms/AdminQuestionForm.vue'),
      },
    ],
  },
];
