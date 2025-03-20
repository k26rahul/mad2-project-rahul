<template>
  <div class="d-flex justify-content-center align-items-center" style="height: 100vh">
    <div class="container p-4 border rounded" style="max-width: 400px">
      <h1 class="mb-4 text-center">Login</h1>
      <form @submit.prevent="submitForm">
        <div class="mb-3">
          <label for="email" class="form-label">Email address</label>
          <input type="email" id="email" class="form-control" v-model="email" required />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input type="password" id="password" class="form-control" v-model="password" required />
        </div>
        <div class="form-check mb-3">
          <input type="checkbox" id="rememberMe" class="form-check-input" v-model="rememberMe" />
          <label for="rememberMe" class="form-check-label">Remember Me</label>
        </div>
        <div v-if="errorMessage" class="alert alert-danger" role="alert">
          {{ errorMessage }}
        </div>
        <button type="submit" class="btn btn-primary w-100">Login</button>
      </form>
    </div>
  </div>
</template>

<script>
import store from '@/store';
import router from '@/router';

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
        const response = await fetch(`${store.api.origin}/api/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
            rememberMe: this.rememberMe,
          }),
        });
        const result = await response.json();
        if (result.success) {
          store.auth.isLoggedIn = true;
          store.auth.role = result.role;
          router.push(result.role === 'admin' ? '/admin' : '/user');
        } else {
          this.errorMessage = result.message;
        }
      } catch (error) {
        this.errorMessage = 'An error occurred. Please try again.';
        console.error('Login failed:', error);
      }
    },
  },
};
</script>
