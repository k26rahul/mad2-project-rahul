import { reactive, watch } from 'vue';

const store = reactive({
  auth: {
    isLoggedIn: false,
    role: null, // 'admin' or 'user'
  },
  api: {
    origin: 'http://127.0.0.1:5000', // Origin URL for API
  },
});

// Restore auth state from local storage
const authStateFromLocalStorage = JSON.parse(localStorage.getItem('authState'));
if (authStateFromLocalStorage) {
  store.auth = { ...store.auth, ...authStateFromLocalStorage };
}

watch(
  () => store.auth,
  newAuthState => {
    localStorage.setItem('authState', JSON.stringify(newAuthState));
  },
  { deep: true }
);

export default store;
