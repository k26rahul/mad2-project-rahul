<template>
  <div>
    <header>
      <h1>User Layout</h1>
      <nav>
        <router-link to="/user/home">Home</router-link>
        <router-link to="/user/scores">Scores</router-link>
      </nav>
    </header>
    <main>
      <router-view></router-view>
    </main>
  </div>
</template>
