<template>
  <div class="container mt-4">
    <!-- Search Controls -->
    <div class="row mb-4">
      <div class="col-md-8">
        <div class="input-group">
          <select v-model="selectedSubjectId" class="form-select flex-grow-0" style="width: 200px">
            <option value="all">All Subjects</option>
            <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
              {{ subject.name }}
            </option>
          </select>
          <select v-model="selectedChapterId" class="form-select flex-grow-0" style="width: 200px">
            <option value="all">All Chapters</option>
            <option v-for="chapter in availableChapters" :key="chapter.id" :value="chapter.id">
              {{ chapter.name }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="text-primary fw-bold">Available Quizzes</h1>
    </div>

    <!-- No quizzes message -->
    <div v-if="filteredQuizzes.length === 0" class="text-center p-5">
      <h3 class="text-muted">No quizzes found</h3>
    </div>

    <!-- Quizzes grid -->
    <div class="row g-4 mb-4">
      <div v-for="quiz in filteredQuizzes" :key="quiz.id" class="col-md-6">
        <div class="card border-0 shadow-lg rounded-4 h-100">
          <!-- Quiz header -->
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
                  'text-success': isQuizStarted(quiz),
                  'text-danger': !isQuizStarted(quiz),
                }"
              >
                <i class="bi bi-calendar me-1"></i>
                {{ formatStartTime(quiz) }}
              </small>
            </div>
          </div>

          <!-- Quiz actions -->
          <div class="card-body">
            <div class="d-flex justify-content-end gap-2">
              <router-link :to="`/user/quiz/${quiz.id}`" class="btn btn-outline-primary">
                <i class="bi bi-eye me-1"></i>
                View Quiz
              </router-link>
              <router-link
                :to="`/user/quiz/${quiz.id}/attempt`"
                class="btn btn-primary"
                :class="{ disabled: !isQuizStarted(quiz) }"
                data-bs-toggle="tooltip"
                data-bs-placement="top"
                :title="!isQuizStarted(quiz) ? 'Quiz has not started yet' : ''"
              >
                <i class="bi bi-play-fill me-1"></i>
                Attempt Quiz
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { subjectStore, chapterStore, quizStore } from '@/store';

export default {
  data() {
    return {
      selectedSubjectId: 'all',
      selectedChapterId: 'all',
      matchingQuizzes: new Set(),
      quizStore,
    };
  },

  computed: {
    subjects() {
      return Array.from(subjectStore.subjects.values());
    },
    chapters() {
      return Array.from(chapterStore.chapters.values());
    },
    quizzes() {
      return Array.from(quizStore.quizzes.values());
    },
    availableChapters() {
      if (this.selectedSubjectId === 'all') {
        return this.chapters;
      }
      return this.chapters.filter(c => c.subject_id === parseInt(this.selectedSubjectId));
    },
    filteredQuizzes() {
      if (this.selectedSubjectId === 'all' && this.selectedChapterId === 'all') {
        return this.quizzes;
      }
      return this.quizzes.filter(q => this.matchingQuizzes.has(q));
    },
  },

  watch: {
    selectedSubjectId() {
      this.selectedChapterId = 'all';
      this.updateQuizMatches();
    },
    selectedChapterId() {
      this.updateQuizMatches();
    },
  },

  methods: {
    updateQuizMatches() {
      this.matchingQuizzes.clear();

      this.quizzes.forEach(quiz => {
        const chapter = chapterStore.chapters.get(quiz.chapter_id);

        const matchesSubject =
          this.selectedSubjectId === 'all' ||
          chapter.subject_id === parseInt(this.selectedSubjectId);

        const matchesChapter =
          this.selectedChapterId === 'all' || quiz.chapter_id === parseInt(this.selectedChapterId);

        if (matchesSubject && matchesChapter) {
          this.matchingQuizzes.add(quiz);
        }
      });
    },

    isQuizStarted(quiz) {
      if (!quiz.start_time) return true;
      return new Date(quiz.start_time) <= new Date();
    },

    formatStartTime(quiz) {
      if (!quiz.start_time) return 'Start anytime';
      const startTime = new Date(quiz.start_time);
      if (this.isQuizStarted(quiz)) {
        return `Started on ${startTime.toLocaleDateString()}`;
      }
      return `Starts on ${startTime.toLocaleString()}`;
    },
  },

  mounted() {
    // Initialize all tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));
  },
};
</script>
