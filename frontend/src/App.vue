<script setup>
import { RouterView } from 'vue-router';
import store from './store';

window.whoami = async () => {
  try {
    const response = await fetch(`${store.api.origin}/api/auth/whoami`, {
      method: 'GET',
      credentials: 'include',
    });
    const result = await response.json();
    console.log('Whoami response:', result);
  } catch (error) {
    console.error('Error fetching whoami:', error);
  }
};
</script>

<template>
  <RouterView></RouterView>
</template>
