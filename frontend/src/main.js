import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './assets/base.css';

createApp(App).use(router).mount('#app');

// debugging
import { get } from '@/utils/fetchHelper';
window.whoami = () => {
  get('/api/auth/whoami');
};
