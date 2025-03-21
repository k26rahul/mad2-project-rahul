<template>
  <div class="d-flex justify-content-center align-items-center bg-light" style="height: 100vh">
    <div class="container p-4 border-0 shadow-lg rounded-4 bg-white" style="max-width: 400px">
      <h1 class="mb-4 text-center text-primary fw-bold">Login</h1>
      <form @submit.prevent="submitForm">
        <div class="mb-3">
          <label for="email" class="form-label fw-semibold">Email address</label>
          <input type="email" id="email" class="form-control shadow-sm" v-model="email" required />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label fw-semibold">Password</label>
          <input
            type="password"
            id="password"
            class="form-control shadow-sm"
            v-model="password"
            required
          />
        </div>
        <div class="form-check mb-3">
          <input type="checkbox" id="rememberMe" class="form-check-input" v-model="rememberMe" />
          <label for="rememberMe" class="form-check-label">Remember Me</label>
        </div>
        <div v-if="errorMessage" class="alert alert-danger shadow-sm" role="alert">
          {{ errorMessage }}
        </div>
        <button type="submit" class="btn btn-primary w-100 shadow-sm">Login</button>
        <button
          type="button"
          class="btn btn-link w-100 mt-2 text-decoration-none"
          @click="goToRegister"
        >
          Don't have an account? <span class="fw-semibold text-primary">Register</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import store from '@/store';
import router from '@/router';
import { post } from '@/utils/fetchHelper';

export default {
  data() {
    return {
      email: '',
      password: '',
      rememberMe: true,
      errorMessage: '', // For displaying error messages
    };
  },
  methods: {
    async submitForm() {
      try {
        const result = await post('/api/auth/login', {
          email: this.email,
          password: this.password,
          rememberMe: this.rememberMe,
        });
        if (result.success) {
          store.auth.isLoggedIn = true;
          store.auth.role = result.role;
          router.push('/');
        } else {
          this.errorMessage = result.message;
        }
      } catch (error) {
        this.errorMessage = 'An error occurred. Please try again.';
      }
    },
    goToRegister() {
      router.push('/register');
    },
  },
};
</script>
