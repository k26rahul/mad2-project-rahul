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
const localStorageAuth = JSON.parse(localStorage.getItem('auth'));
if (localStorageAuth) {
  store.auth = { ...store.auth, ...localStorageAuth };
}

// Watch for auth changes and save to local storage
watch(
  () => store.auth,
  newAuthState => {
    localStorage.setItem('auth', JSON.stringify(newAuthState));
  },
  { deep: true }
);

export default store;
