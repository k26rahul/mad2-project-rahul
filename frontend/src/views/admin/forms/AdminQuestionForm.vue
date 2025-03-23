<template>
  <div class="container p-4 border-0 shadow-lg rounded-4 bg-white" style="max-width: 600px">
    <h1 class="text-center mb-4">{{ isEdit ? 'Edit Question' : 'Create New Question' }}</h1>

    <div class="card bg-light mb-4">
      <div class="card-body">
        <h6 class="card-subtitle mb-2 text-muted">Quiz Details</h6>
        <h5 class="card-title">{{ quizTitle }}</h5>
        <p class="card-text mb-0">Subject: {{ subjectName }}</p>
        <p class="card-text">Chapter: {{ chapterName }}</p>
      </div>
    </div>

    <form @submit.prevent="handleSubmit">
      <div class="mb-3">
        <label class="form-label fw-semibold">Question Statement</label>
        <textarea
          class="form-control shadow-sm"
          v-model="formData.statement"
          rows="3"
          required
        ></textarea>
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold">Option A</label>
        <input type="text" class="form-control shadow-sm" v-model="formData.option_a" required />
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold">Option B</label>
        <input type="text" class="form-control shadow-sm" v-model="formData.option_b" required />
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold">Option C</label>
        <input type="text" class="form-control shadow-sm" v-model="formData.option_c" required />
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold">Option D</label>
        <input type="text" class="form-control shadow-sm" v-model="formData.option_d" required />
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold">Correct Option</label>
        <select class="form-select shadow-sm" v-model="formData.correct_option" required>
          <option value="">Select Correct Option</option>
          <option value="1">Option A</option>
          <option value="2">Option B</option>
          <option value="3">Option C</option>
          <option value="4">Option D</option>
        </select>
      </div>

      <div v-if="errorMessage" class="alert alert-danger shadow-sm" role="alert">
        {{ errorMessage }}
      </div>

      <button type="submit" class="btn btn-primary w-100 shadow-sm">
        {{ isEdit ? 'Update Question' : 'Create Question' }}
      </button>
    </form>
  </div>
</template>

<script>
import { questionStore, quizStore, subjectStore, chapterStore } from '@/store';
import router from '@/router';

export default {
  data() {
    return {
      formData: {
        statement: '',
        option_a: '',
        option_b: '',
        option_c: '',
        option_d: '',
        correct_option: '',
        quiz_id: '',
      },
      quizTitle: '',
      subjectName: '',
      chapterName: '',
      errorMessage: '',
    };
  },
  computed: {
    isEdit() {
      return this.$route.name === 'AdminQuestionEdit';
    },
  },
  async created() {
    if (this.isEdit) {
      const id = this.$route.params.id;
      const question = questionStore.questions.get(parseInt(id));
      if (question) {
        this.formData = {
          statement: question.statement,
          option_a: question.option_a,
          option_b: question.option_b,
          option_c: question.option_c,
          option_d: question.option_d,
          correct_option: question.correct_option,
          quiz_id: question.quiz_id,
        };
        await this.loadQuizData(question.quiz_id);
      }
    } else {
      this.formData.quiz_id = this.$route.params.quiz_id;
      await this.loadQuizData(this.$route.params.quiz_id);
    }
  },
  methods: {
    async loadQuizData(quizId) {
      const quiz = quizStore.quizzes.get(parseInt(quizId));
      if (quiz) {
        this.quizTitle = quiz.title;
        this.subjectName = quiz.subject_name;
        this.chapterName = quiz.chapter_name;
      }
    },
    async handleSubmit() {
      try {
        if (this.isEdit) {
          await questionStore.update(this.$route.params.id, this.formData);
        } else {
          await questionStore.create(this.formData);
        }
        router.push('/admin/quizzes');
      } catch (error) {
        this.errorMessage = 'An error occurred while submitting the form.';
      }
    },
  },
};
</script>
