<template>
  <div>
    <header class="bg-primary text-white py-3 shadow-sm">
      <div class="container d-flex justify-content-between align-items-center">
        <RouterLink to="/admin/home" class="text-white text-decoration-none">
          <h1 class="h3 mb-0 fw-bold">Admin Dashboard</h1>
        </RouterLink>
        <nav>
          <ul class="nav">
            <li class="nav-item">
              <RouterLink to="/admin/home" class="nav-link text-white fw-semibold">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/admin/quizzes" class="nav-link text-white fw-semibold"
                >Quizzes</RouterLink
              >
            </li>
            <li class="nav-item">
              <RouterLink to="/admin/users" class="nav-link text-white fw-semibold"
                >Users</RouterLink
              >
            </li>
            <li class="nav-item">
              <RouterLink to="/admin/summary" class="nav-link text-white fw-semibold"
                >Summary</RouterLink
              >
            </li>
          </ul>
        </nav>
      </div>
    </header>
    <main class="container mt-4">
      <div
        v-if="loading"
        class="d-flex justify-content-center align-items-center"
        style="height: 80vh"
      >
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <div v-else>
        <RouterView></RouterView>
      </div>
    </main>
  </div>
</template>

<script>
import { RouterLink, RouterView } from 'vue-router';
import { subjectStore, quizStore, questionStore, chapterStore } from '@/store';

export default {
  components: {
    RouterLink,
    RouterView,
  },
  data() {
    return {
      loading: true,
    };
  },
  async created() {
    await Promise.all([
      subjectStore.fetchAll(),
      quizStore.fetchAll(),
      questionStore.fetchAll(),
      chapterStore.fetchAll(),
    ]);
    this.loading = false;
  },
};
</script>
