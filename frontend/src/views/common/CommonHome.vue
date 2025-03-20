<template>
  <div class="container text-center mt-5">
    <h1 class="mb-4">Welcome to Quiz Master V2</h1>
    <p class="lead">
      Quiz Master V2 is a multi-user exam preparation application designed to manage and attempt
      quizzes across multiple subjects. It supports two roles:
      <strong>Admin (Quiz Master)</strong> and <strong>Users (Students)</strong>.
    </p>
    <div class="row mt-5">
      <div class="col-md-6">
        <h3>For Students</h3>
        <p>
          - Register and log in to access quizzes.<br />
          - Attempt quizzes across multiple subjects and chapters.<br />
          - View your scores and quiz history.<br />
          - Export your quiz results as CSV for future reference.
        </p>
      </div>
      <div class="col-md-6">
        <h3>For Admins</h3>
        <p>
          - Manage users, subjects, chapters, and quizzes.<br />
          - Create and edit quizzes with ease.<br />
          - View detailed reports and export data as CSV.<br />
          - Monitor quiz participation and performance.
        </p>
      </div>
    </div>
    <div class="mt-5">
      <router-link to="/login" class="btn btn-primary btn-lg me-2">Login</router-link>
      <router-link to="/register" class="btn btn-secondary btn-lg">Register</router-link>
    </div>
  </div>
</template>

<script>
import store from '@/store';
import router from '@/router';

export default {
  created() {
    if (store.auth.isLoggedIn) {
      router.push(store.auth.role === 'admin' ? '/admin' : '/user');
    }
  },
};
</script>
