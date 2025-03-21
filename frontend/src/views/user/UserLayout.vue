<template>
  <div>
    <header class="bg-primary text-white py-3 shadow-sm">
      <div class="container d-flex justify-content-between align-items-center">
        <h1 class="h3 mb-0 fw-bold">User Dashboard</h1>
        <nav>
          <ul class="nav">
            <li class="nav-item">
              <RouterLink to="/user/home" class="nav-link text-white fw-semibold">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/user/scores" class="nav-link text-white fw-semibold"
                >Scores</RouterLink
              >
            </li>
            <li class="nav-item">
              <RouterLink to="/user/search" class="nav-link text-white fw-semibold"
                >Search</RouterLink
              >
            </li>
            <li class="nav-item">
              <RouterLink to="/user/summary" class="nav-link text-white fw-semibold"
                >Summary</RouterLink
              >
            </li>
          </ul>
        </nav>
      </div>
    </header>
    <main class="container mt-4">
      <RouterView></RouterView>
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>
