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
import { post, put, get } from '@/utils/fetchHelper';
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
      isEdit: false,
    };
  },
  async created() {
    const id = this.$route.params.id;
    if (id) {
      this.isEdit = true;
      await this.loadQuestionData(id);
    } else {
      this.formData.quiz_id = this.$route.params.quiz_id;
      await this.loadQuizData(this.$route.params.quiz_id);
    }
  },
  methods: {
    async loadQuizData(quizId) {
      try {
        const result = await get(`/api/quiz/get/${quizId}`);
        if (result.success) {
          this.quizTitle = result.quiz.title;
          this.subjectName = result.quiz.subject_name;
          this.chapterName = result.quiz.chapter_name;
        }
      } catch (error) {
        this.errorMessage = 'Failed to load quiz data';
      }
    },
    async loadQuestionData(id) {
      try {
        const result = await get(`/api/question/get/${id}`);
        if (result.success) {
          this.formData = {
            statement: result.question.statement,
            option_a: result.question.option_a,
            option_b: result.question.option_b,
            option_c: result.question.option_c,
            option_d: result.question.option_d,
            correct_option: result.question.correct_option,
            quiz_id: result.question.quiz_id,
          };
          this.quizTitle = result.question.quiz_title;
          this.subjectName = result.question.subject_name;
          this.chapterName = result.question.chapter_name;
        }
      } catch (error) {
        this.errorMessage = 'Failed to load question data';
      }
    },
    async handleSubmit() {
      try {
        let result;
        if (this.isEdit) {
          result = await put(`/api/question/update/${this.$route.params.id}`, this.formData);
        } else {
          result = await post('/api/question/create', this.formData);
        }

        if (result.success) {
          router.push('/admin/quizzes');
        } else {
          this.errorMessage = result.message;
        }
      } catch (error) {
        this.errorMessage = 'An error occurred. Please try again.';
      }
    },
  },
};
</script>
