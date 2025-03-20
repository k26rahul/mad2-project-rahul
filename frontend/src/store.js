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

// Restore state from local storage
const savedState = JSON.parse(localStorage.getItem('store'));
if (savedState) {
  // Object.assign(store, savedState);
}

// Watch for changes and save to local storage
watch(
  () => store,
  newState => {
    localStorage.setItem('store', JSON.stringify(newState));
  },
  { deep: true }
);

export default store;
