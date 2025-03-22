import { get } from '@/utils/fetchHelper';
import store from '@/store';
import router from '@/router';

(window.whoami = async () => {
  const response = await get('/api/auth/whoami');

  if (store.auth.isLoggedIn && !response.success) {
    store.auth.isLoggedIn = false;
    store.auth.role = null;
    console.log('User is not authenticated, redirecting to login page');
    router.push('/login');
  }
})();
