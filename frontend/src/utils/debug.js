import { get } from '@/utils/fetchHelper';
import { authStore } from '@/store';
import router from '@/router';

(window.whoami = async () => {
  const response = await get('/api/auth/whoami');

  if (authStore.isLoggedIn && !response.success) {
    authStore.isLoggedIn = false;
    authStore.role = null;
    router.push('/login');
  }
})();
