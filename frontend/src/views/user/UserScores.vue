<template>
  <div class="container mt-4">
    <h1 class="text-primary fw-bold mb-4">Your Quiz Scores</h1>

    <!-- No attempts message -->
    <div v-if="groupedAttempts.length === 0" class="text-center p-5">
      <h3 class="text-muted">No quiz attempts yet</h3>
      <p class="lead">Start attempting quizzes to see your scores here!</p>
      <router-link to="/user/home" class="btn btn-primary btn-lg">
        <i class="bi bi-play-fill me-1"></i>
        Browse Quizzes
      </router-link>
    </div>

    <!-- Grouped attempts list -->
    <div v-else class="row g-4">
      <div v-for="group in groupedAttempts" :key="group.quiz_id" class="col-12">
        <!-- Quiz header card -->
        <div class="card border-0 shadow-lg rounded-4 mb-3">
          <div class="card-header bg-primary bg-opacity-10 border-0 rounded-top-4">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h4 class="fw-bold mb-1">{{ group.quiz_title }}</h4>
                <small class="text-secondary">
                  <i class="bi bi-journal me-1"></i>
                  {{ group.chapter_name }} ({{ group.subject_name }})
                </small>
              </div>
              <router-link :to="`/user/quiz/${group.quiz_id}`" class="btn btn-outline-primary">
                <i class="bi bi-eye me-1"></i>
                View Quiz
              </router-link>
            </div>
          </div>
        </div>

        <!-- Attempts for this quiz -->
        <div class="mb-4">
          <!-- Latest attempt (always visible) -->
          <div v-if="group.attempts.length > 0" class="mx-4">
            <div class="card border-start border-4 border-primary bg-light">
              <div class="card-body">
                <div class="d-flex align-items-center gap-2 mb-3">
                  <small class="text-primary">
                    <i class="bi bi-star-fill me-1"></i>
                    Latest Attempt
                  </small>
                  <small v-if="isBestAttempt(group, group.attempts[0])" class="text-warning">
                    <i class="bi bi-trophy-fill me-1"></i>
                    Best Score
                  </small>
                </div>
                <div class="row align-items-center">
                  <div class="col-md-3">
                    <small class="text-muted">
                      <i class="bi bi-clock-history me-1"></i>
                      {{ new Date(group.attempts[0].attempted_at).toLocaleString() }}
                    </small>
                  </div>

                  <div class="col-md-6">
                    <div class="d-flex gap-4 justify-content-center">
                      <div class="text-center">
                        <div class="h4 mb-0">{{ group.attempts[0].correct_questions }}</div>
                        <small class="text-success">Correct</small>
                      </div>
                      <div class="text-center">
                        <div class="h4 mb-0">{{ group.attempts[0].incorrect_questions }}</div>
                        <small class="text-danger">Incorrect</small>
                      </div>
                      <div class="text-center">
                        <div class="h4 mb-0">{{ group.attempts[0].total_questions }}</div>
                        <small class="text-muted">Total</small>
                      </div>
                    </div>
                  </div>

                  <div class="col-md-3 text-end">
                    <h3 class="mb-0" :class="getScoreClass(group.attempts[0].percentage)">
                      {{ group.attempts[0].percentage.toFixed(1) }}%
                    </h3>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Older attempts in accordion -->
          <div
            v-if="group.attempts.length > 1"
            class="accordion mx-4"
            :id="`accordion${group.quiz_id}`"
          >
            <div class="accordion-item border-0">
              <h2 class="accordion-header">
                <button
                  class="accordion-button collapsed bg-transparent"
                  type="button"
                  data-bs-toggle="collapse"
                  :data-bs-target="`#collapse${group.quiz_id}`"
                >
                  <small class="text-muted">
                    <i class="bi bi-clock-history me-1"></i>
                    {{ group.attempts.length - 1 }} Previous Attempts
                  </small>
                </button>
              </h2>
              <div
                :id="`collapse${group.quiz_id}`"
                class="accordion-collapse collapse"
                :data-bs-parent="`#accordion${group.quiz_id}`"
              >
                <div class="accordion-body p-0 pt-3">
                  <div
                    v-for="attempt in group.attempts.slice(1)"
                    :key="attempt.id"
                    class="card border-start border-4 border-primary bg-light mb-3"
                  >
                    <div class="card-body">
                      <div
                        v-if="isBestAttempt(group, attempt)"
                        class="d-flex align-items-center gap-2 mb-3"
                      >
                        <small class="text-warning">
                          <i class="bi bi-trophy-fill me-1"></i>
                          Best Score
                        </small>
                      </div>
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
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { quizAttemptStore } from '@/store';

export default {
  computed: {
    groupedAttempts() {
      // Get all attempts
      const attempts = Array.from(quizAttemptStore.attempts.values());

      // Group by quiz_id
      const groups = new Map();
      attempts.forEach(attempt => {
        if (!groups.has(attempt.quiz_id)) {
          groups.set(attempt.quiz_id, {
            quiz_id: attempt.quiz_id,
            quiz_title: attempt.quiz_title,
            chapter_name: attempt.chapter_name,
            subject_name: attempt.subject_name,
            attempts: [],
          });
        }
        groups.get(attempt.quiz_id).attempts.push(attempt);
      });

      // Sort attempts within each group by date (newest first)
      groups.forEach(group => {
        group.attempts.sort((a, b) => new Date(b.attempted_at) - new Date(a.attempted_at));
      });

      // Convert to array and sort groups by most recent attempt
      return Array.from(groups.values()).sort((a, b) => {
        const latestA = new Date(a.attempts[0]?.attempted_at || 0);
        const latestB = new Date(b.attempts[0]?.attempted_at || 0);
        return latestB - latestA;
      });
    },
  },

  methods: {
    getScoreClass(percentage) {
      if (percentage >= 80) return 'text-success';
      if (percentage >= 60) return 'text-primary';
      if (percentage >= 40) return 'text-warning';
      return 'text-danger';
    },

    isBestAttempt(group, attempt) {
      return !group.attempts.some(a => a.percentage > attempt.percentage);
    },
  },
};
</script>
