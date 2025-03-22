<template>
  <div class="container text-center mt-5">
    <div class="card shadow-lg p-5 border-0 rounded-4">
      <div class="display-1 text-primary mb-3">404</div>
      <div class="display-4 mb-4 text-secondary">Page Not Found</div>
      <div class="lead text-muted mb-5">
        Oops! The page you're looking for seems to have vanished into thin air.
      </div>
      <div>
        <router-link to="/" class="btn btn-primary btn-lg shadow-sm">
          <i class="bi bi-house-door me-2"></i>Return Home
        </router-link>
      </div>
    </div>
    <div class="mt-4 text-muted">
      <small>Lost? Don't worry, it happens to the best of us.</small>
    </div>
  </div>
</template>
