<template>
  <div class="d-flex justify-content-center align-items-center bg-light" style="height: 100vh">
    <div class="container p-4 border-0 shadow-lg rounded-4 bg-white" style="max-width: 400px">
      <h1 class="mb-4 text-center text-primary fw-bold">Register</h1>
      <form @submit.prevent="submitForm">
        <div class="mb-3">
          <label for="name" class="form-label fw-semibold">Name</label>
          <input type="text" id="name" class="form-control shadow-sm" v-model="name" required />
        </div>
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
        <div class="mb-3">
          <label for="dob" class="form-label fw-semibold">Date of Birth</label>
          <input type="date" id="dob" class="form-control shadow-sm" v-model="dob" />
        </div>
        <div class="mb-3">
          <label for="qualification" class="form-label fw-semibold">Qualification</label>
          <select id="qualification" class="form-select shadow-sm" v-model="qualification">
            <option value="" disabled>Select your qualification</option>
            <option value="High School">High School</option>
            <option value="Bachelor's">Bachelor's</option>
            <option value="Master's">Master's</option>
            <option value="PhD">PhD</option>
            <option value="Other">Other</option>
          </select>
        </div>
        <div v-if="errorMessage" class="alert alert-danger shadow-sm" role="alert">
          {{ errorMessage }}
        </div>
        <button type="submit" class="btn btn-primary w-100 shadow-sm">Register</button>
        <button
          type="button"
          class="btn btn-link w-100 mt-2 text-decoration-none"
          @click="goToLogin"
        >
          Already have an account? <span class="fw-semibold text-primary">Login</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import store from '@/store/store/store';
import router from '@/router';
import { post } from '@/utils/fetchHelper';

export default {
  data() {
    return {
      name: '',
      email: '',
      password: '',
      dob: '',
      qualification: '',
      errorMessage: '',
    };
  },
  methods: {
    async submitForm() {
      try {
        const result = await post('/api/auth/register', {
          name: this.name,
          email: this.email,
          password: this.password,
          dob: this.dob,
          qualification: this.qualification,
        });
        if (result.success) {
          store.auth.isLoggedIn = true;
          store.auth.role = 'user';
          router.push('/');
        } else {
          this.errorMessage = result.message;
        }
      } catch (error) {
        this.errorMessage = 'An error occurred. Please try again.';
      }
    },
    goToLogin() {
      router.push('/login');
    },
  },
};
</script>
