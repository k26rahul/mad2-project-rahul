<template>
  <div>
    <header class="bg-primary text-white py-3 shadow-sm">
      <div class="container d-flex justify-content-between align-items-center">
        <RouterLink to="/user/home" class="text-white text-decoration-none">
          <h1 class="h3 mb-0 fw-bold">User Dashboard</h1>
        </RouterLink>
        <nav>
          <ul class="nav">
            <li class="nav-item">
              <RouterLink
                to="home"
                class="nav-link text-white fw-semibold"
                :class="{
                  'border-bottom border-2 border-white opacity-100': isHomeActive,
                  'opacity-75': !isHomeActive,
                }"
                >Home</RouterLink
              >
            </li>
            <li class="nav-item">
              <RouterLink
                to="scores"
                class="nav-link text-white fw-semibold"
                :class="{
                  'border-bottom border-2 border-white opacity-100': isScoresActive,
                  'opacity-75': !isScoresActive,
                }"
                >Scores</RouterLink
              >
            </li>
            <li class="nav-item">
              <RouterLink
                to="summary"
                class="nav-link text-white fw-semibold"
                :class="{
                  'border-bottom border-2 border-white opacity-100': isSummaryActive,
                  'opacity-75': !isSummaryActive,
                }"
                >Summary</RouterLink
              >
            </li>
            <li class="nav-item">
              <a href="#" @click.prevent="logout" class="nav-link text-white fw-semibold">
                <i class="bi bi-box-arrow-right me-1"></i>Logout
              </a>
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
import { subjectStore, quizStore, questionStore, chapterStore, authStore } from '@/store';
import { post } from '@/utils/fetchHelper';
import router from '@/router';

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
  computed: {
    isHomeActive() {
      return this.$route.path === '/user/home';
    },
    isScoresActive() {
      return this.$route.path === '/user/scores';
    },
    isSummaryActive() {
      return this.$route.path === '/user/summary';
    },
  },
  methods: {
    async logout() {
      try {
        const result = await post('/api/auth/logout');
        if (result.success) {
          authStore.isLoggedIn = false;
          authStore.role = null;
          router.push('/login');
        }
      } catch (error) {
        console.error('Logout failed:', error);
      }
    },
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
