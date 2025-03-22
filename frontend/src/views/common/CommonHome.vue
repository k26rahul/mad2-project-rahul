<template>
  <div class="container text-center mt-5">
    <div class="card shadow-lg p-4 border-0 rounded-4">
      <h1 class="mb-4 text-primary fw-bold">Welcome to Quiz Master V2</h1>
      <p class="lead text-muted">
        Quiz Master V2 is a multi-user exam preparation platform supporting two roles:
        <strong class="text-dark">Admin (Quiz Master)</strong> and
        <strong class="text-dark">Users (Students)</strong>.
      </p>
      <div class="mt-4">
        <router-link to="/login" class="btn btn-primary btn-lg me-2 shadow-sm">
          <i class="bi bi-box-arrow-in-right me-2"></i>Login
        </router-link>
        <router-link to="/register" class="btn btn-outline-primary btn-lg shadow-sm">
          <i class="bi bi-person-plus me-2"></i>Register
        </router-link>
      </div>
    </div>

    <h2 class="mt-5 text-secondary fw-bold">Features</h2>
    <div class="row my-4">
      <div class="col-md-6">
        <div class="card border-0 shadow-sm p-3 mb-4 rounded-4 h-100">
          <h3 class="text-success fw-semibold">
            <i class="bi bi-mortarboard me-2"></i>For Students
          </h3>
          <ul class="list-unstyled text-muted">
            <li>✔ Register and log in to access quizzes.</li>
            <li>✔ Attempt quizzes across multiple subjects and chapters.</li>
            <li>✔ View your scores and quiz history.</li>
            <li>✔ Export quiz results as CSV for future reference.</li>
          </ul>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card border-0 shadow-sm p-3 mb-4 rounded-4 h-100">
          <h3 class="text-danger fw-semibold"><i class="bi bi-shield-lock me-2"></i>For Admins</h3>
          <ul class="list-unstyled text-muted">
            <li>✔ Manage users, subjects, chapters, and quizzes.</li>
            <li>✔ Create and edit quizzes with ease.</li>
            <li>✔ View detailed reports and export data as CSV.</li>
            <li>✔ Monitor quiz participation and performance.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
