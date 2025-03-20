<script setup>
import { RouterView } from 'vue-router';
import { get } from '@/utils/fetchHelper';

window.whoami = () => {
  get('/api/auth/whoami');
};
</script>

<template>
  <RouterView></RouterView>
</template>
