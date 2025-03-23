<template>
  <div class="container mt-4">
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
      <h1 class="text-primary fw-bold">Quizzes</h1>
      <router-link to="/admin/quiz/new" class="btn btn-primary shadow-sm">
        <i class="bi bi-plus-lg fs-5"></i> Add Quiz
      </router-link>
    </div>

    <!-- No quizzes message -->
    <div v-if="quizzes.filter(q => q.$matches).length === 0" class="text-center p-5">
      <h3 class="text-muted">No quizzes found</h3>
      <p class="lead" v-if="quizzes.length === 0">Start by adding a new quiz</p>
    </div>

    <!-- Quizzes grid -->
    <div class="row g-4 mb-4">
      <div v-for="quiz in quizzes.filter(q => q.$matches)" :key="quiz.id" class="col-md-6">
        <div class="card border-0 shadow-lg rounded-4 h-100">
          <!-- Quiz header -->
          <div class="card-header bg-primary bg-opacity-10 border-0 rounded-top-4">
            <div class="d-flex justify-content-between align-items-center">
              <h3 class="fw-bold mb-0">{{ quiz.title }}</h3>
              <div class="btn-group">
                <button @click="editQuiz(quiz.id)" class="btn btn-sm btn-outline-primary">
                  <i class="bi bi-pencil fs-5"></i>
                </button>
                <button @click="deleteQuiz(quiz.id)" class="btn btn-sm btn-outline-danger">
                  <i class="bi bi-trash fs-5"></i>
                </button>
              </div>
            </div>
            <p class="text-muted mb-2">{{ quiz.description }}</p>
            <div class="d-flex gap-3">
              <small class="text-secondary">
                <i class="bi bi-journal me-1"></i>
                {{ quiz.chapter_name }} ({{ quiz.subject_name }})
              </small>
              <small class="text-secondary" v-if="quiz.duration">
                <i class="bi bi-clock me-1"></i>
                {{ quiz.duration }} minutes
              </small>
              <small class="text-secondary" v-if="quiz.start_time">
                <i class="bi bi-calendar me-1"></i>
                {{ new Date(quiz.start_time).toLocaleString() }}
              </small>
            </div>
          </div>

          <!-- Questions list -->
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h4 class="text-secondary fw-semibold">Questions</h4>
              <router-link
                :to="`/admin/quiz/${quiz.id}/question/new`"
                class="btn btn-sm btn-outline-primary"
              >
                <i class="bi bi-plus-lg fs-5"></i> Add Question
              </router-link>
            </div>

            <!-- No questions message -->
            <div v-if="!quiz.questions.length" class="text-center p-3">
              <p class="text-muted mb-0">No questions yet</p>
            </div>

            <!-- Questions -->
            <div v-else class="list-group list-group-flush">
              <div
                v-for="question in quiz.questions"
                :key="question.id"
                class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
              >
                <div class="pe-2">
                  <p class="mb-0">{{ question.statement }}</p>
                </div>
                <div class="btn-group flex-shrink-0">
                  <button
                    @click="editQuestion(question.id)"
                    class="btn btn-sm btn-outline-secondary"
                  >
                    <i class="bi bi-pencil fs-5"></i>
                  </button>
                  <button
                    @click="deleteQuestion(question.id, quiz.id)"
                    class="btn btn-sm btn-outline-danger"
                  >
                    <i class="bi bi-trash fs-5"></i>
                  </button>
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
import store from '@/store/store/store';

export default {
  data() {
    return {
      selectedSubjectId: 'all',
      selectedChapterId: 'all',
    };
  },

  computed: {
    subjects() {
      return store.subjects;
    },
    quizzes() {
      return store.quizzes;
    },
    availableChapters() {
      if (this.selectedSubjectId === 'all') {
        return this.subjects.flatMap(s => s.chapters);
      }
      const subject = this.subjects.find(s => s.id === this.selectedSubjectId);
      return subject ? subject.chapters : [];
    },
  },

  watch: {
    selectedSubjectId(newVal) {
      this.selectedChapterId = 'all';
      this.updateQuizMatches();
    },
    selectedChapterId() {
      this.updateQuizMatches();
    },
  },

  async created() {
    await Promise.all([store.subjects.fetchAll(), store.quizzes.fetchAll()]);
    this.updateQuizMatches();
  },

  methods: {
    updateQuizMatches() {
      this.quizzes.forEach(quiz => {
        const matchesSubject =
          this.selectedSubjectId === 'all' ||
          this.subjects.some(
            s => s.id === this.selectedSubjectId && s.chapters.some(c => c.id === quiz.chapter_id)
          );

        const matchesChapter =
          this.selectedChapterId === 'all' || quiz.chapter_id === this.selectedChapterId;

        quiz.$matches = matchesSubject && matchesChapter;
      });
    },

    editQuiz(id) {
      this.$router.push(`/admin/quiz/${id}/edit`);
    },

    async deleteQuiz(id) {
      if (!confirm('Are you sure you want to delete this quiz and all its questions?')) return;
      await store.quizzes.delete(id);
    },

    editQuestion(id) {
      this.$router.push(`/admin/question/${id}/edit`);
    },

    async deleteQuestion(id) {
      if (!confirm('Are you sure you want to delete this question?')) return;
      await store.questions.delete(id);
    },
  },
};
</script>
