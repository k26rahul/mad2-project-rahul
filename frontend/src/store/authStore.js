import { reactive, watch } from 'vue';

const authStore = reactive({ isLoggedIn: false, role: null });

const authStateFromLocalStorage = JSON.parse(localStorage.getItem('authState'));
if (authStateFromLocalStorage) {
  authStore.isLoggedIn = authStateFromLocalStorage.isLoggedIn;
  authStore.role = authStateFromLocalStorage.role;
}

watch(
  () => authStore,
  ns => {
    localStorage.setItem('authState', JSON.stringify(ns));
  },
  { deep: true }
);

export default authStore;
