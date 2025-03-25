<template>
  <div class="container mt-4">
    <!-- Quiz Details Card -->
    <div class="card border-0 shadow-lg rounded-4 mb-4">
      <div class="card-header bg-primary bg-opacity-10 border-0 rounded-top-4">
        <div class="d-flex justify-content-between align-items-center">
          <h3 class="fw-bold mb-0">{{ quiz.title }}</h3>
          <div class="quiz-stats d-flex gap-2">
            <span class="badge bg-success">
              <i class="bi bi-question-circle me-1"></i>
              {{ quizStore.getQuestionsForQuiz(quiz).length }} Questions
            </span>
            <span class="badge bg-info">
              <i class="bi bi-trophy me-1"></i>
              {{ quizStore.getQuestionsForQuiz(quiz).length }} Marks
            </span>
          </div>
        </div>
        <p class="text-muted mb-2">{{ quiz.description }}</p>
        <div class="d-flex gap-3">
          <small class="text-secondary">
            <i class="bi bi-journal me-1"></i>
            {{ quiz.chapter_name }} ({{ quiz.subject_name }})
          </small>
          <small class="text-secondary">
            <i class="bi bi-clock me-1"></i>
            {{ quiz.duration ? `${quiz.duration} minutes` : 'No time limit' }}
          </small>
          <small
            :class="{
              'text-success': isQuizStarted,
              'text-warning': !isQuizStarted,
            }"
          >
            <i class="bi bi-calendar me-1"></i>
            {{ formatStartTime }}
          </small>
        </div>
      </div>
      <div class="card-body">
        <div class="d-flex justify-content-center">
          <router-link
            :to="`/user/quiz/${quiz.id}/attempt`"
            class="btn btn-primary btn-lg"
            :class="{ disabled: !isQuizStarted }"
            data-bs-toggle="tooltip"
            data-bs-placement="top"
            :title="!isQuizStarted ? 'Quiz has not started yet' : ''"
          >
            <i class="bi bi-play-fill me-1"></i>
            Attempt Quiz
          </router-link>
        </div>
      </div>
    </div>

    <!-- Previous Attempts Section -->
    <h2 class="mb-4 text-secondary fw-bold">Previous Attempts</h2>
    <div v-if="quizAttempts.length === 0" class="text-center p-5">
      <h3 class="text-muted">No attempts yet</h3>
      <p class="lead">Be the first one to attempt this quiz!</p>
    </div>

    <div v-else class="row g-4 mb-4">
      <div v-for="attempt in quizAttempts" :key="attempt.id" class="col-12">
        <div class="card border-0 shadow-sm rounded-4">
          <div class="card-body">
            <div class="row align-items-center">
              <div class="col-md-3">
                <small class="text-muted">
                  <i class="bi bi-clock-history me-1"></i>
                  {{ new Date(attempt.attempted_at).toLocaleString() }}
                </small>
              </div>
              <div class="col-md-6">
                <div class="d-flex gap-4 justify-content-center">
                  <div class="text-center">
                    <div class="h4 mb-0">{{ attempt.correct_questions }}</div>
                    <small class="text-success">Correct</small>
                  </div>
                  <div class="text-center">
                    <div class="h4 mb-0">{{ attempt.incorrect_questions }}</div>
                    <small class="text-danger">Incorrect</small>
                  </div>
                  <div class="text-center">
                    <div class="h4 mb-0">{{ attempt.total_questions }}</div>
                    <small class="text-muted">Total</small>
                  </div>
                </div>
              </div>
              <div class="col-md-3 text-end">
                <h3 class="mb-0" :class="getScoreClass(attempt.percentage)">
                  {{ attempt.percentage.toFixed(1) }}%
                </h3>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { quizStore, quizAttemptStore } from '@/store';

export default {
  data() {
    return {
      quiz: quizStore.quizzes.get(parseInt(this.$route.params.quiz_id)),
      quizStore,
    };
  },

  computed: {
    quizAttempts() {
      // Get attempts for this quiz, sorted by date (newest first)
      return Array.from(quizAttemptStore.attempts.values())
        .filter(attempt => attempt.quiz_id === this.quizId)
        .sort((a, b) => new Date(b.attempted_at) - new Date(a.attempted_at));
    },

    quizId() {
      return parseInt(this.$route.params.quiz_id);
    },

    isQuizStarted() {
      if (!this.quiz?.start_time) return true;
      return new Date(this.quiz.start_time) <= new Date();
    },

    formatStartTime() {
      if (!this.quiz?.start_time) return 'Start anytime';
      const startTime = new Date(this.quiz.start_time);
      if (this.isQuizStarted) {
        return `Started on ${startTime.toLocaleDateString()}`;
      }
      return `Starts on ${startTime.toLocaleString()}`;
    },
  },

  methods: {
    getScoreClass(percentage) {
      if (percentage >= 80) return 'text-success';
      if (percentage >= 60) return 'text-primary';
      if (percentage >= 40) return 'text-warning';
      return 'text-danger';
    },
  },

  mounted() {
    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));
  },
};
</script>
