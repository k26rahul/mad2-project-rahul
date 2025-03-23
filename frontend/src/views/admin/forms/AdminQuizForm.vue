<template>
  <div class="container p-4 border-0 shadow-lg rounded-4 bg-white" style="max-width: 600px">
    <h1 class="text-center mb-4">{{ isEdit ? 'Edit Quiz' : 'Create New Quiz' }}</h1>
    <form @submit.prevent="handleSubmit">
      <div class="mb-3">
        <label class="form-label fw-semibold">Subject</label>
        <select
          class="form-select shadow-sm"
          v-model="selectedSubject"
          @change="loadChapters"
          :disabled="isEdit"
        >
          <option :value="null">Select Subject</option>
          <option v-for="subject in subjects" :key="subject.id" :value="subject">
            {{ subject.name }}
          </option>
        </select>
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold">Chapter</label>
        <select class="form-select shadow-sm" v-model="formData.chapter_id" :disabled="isEdit">
          <option value="">Select Chapter</option>
          <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">
            {{ chapter.name }}
          </option>
        </select>
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold">Quiz Title</label>
        <input type="text" class="form-control shadow-sm" v-model="formData.title" required />
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold">Description</label>
        <textarea class="form-control shadow-sm" v-model="formData.description" rows="3"></textarea>
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold">Start Time</label>
        <input type="datetime-local" class="form-control shadow-sm" v-model="formData.start_time" />
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold">Duration (minutes)</label>
        <input type="number" class="form-control shadow-sm" v-model="formData.duration" />
      </div>

      <div v-if="errorMessage" class="alert alert-danger shadow-sm" role="alert">
        {{ errorMessage }}
      </div>

      <button type="submit" class="btn btn-primary w-100 shadow-sm">
        {{ isEdit ? 'Update Quiz' : 'Create Quiz' }}
      </button>
    </form>
  </div>
</template>

<script>
import { quizStore, subjectStore } from '@/store';
import router from '@/router';

export default {
  data() {
    return {
      formData: {
        title: '',
        description: '',
        chapter_id: '',
        start_time: '',
        duration: '',
      },
      selectedSubject: null,
      errorMessage: '',
    };
  },
  computed: {
    subjects() {
      return Array.from(subjectStore.subjects.values());
    },
    chapters() {
      return this.selectedSubject ? subjectStore.getChaptersForSubject(this.selectedSubject) : [];
    },
    isEdit() {
      return this.$route.name === 'AdminQuizEdit';
    },
  },
  async created() {
    if (this.isEdit) {
      const id = this.$route.params.id;
      const quiz = quizStore.quizzes.get(parseInt(id));
      if (quiz) {
        this.formData = {
          title: quiz.title,
          description: quiz.description,
          chapter_id: quiz.chapter_id,
          start_time: quiz.start_time ? quiz.start_time : '',
          duration: quiz.duration,
        };
        this.selectedSubject = this.subjects.find(s => s.chapters.includes(quiz.chapter_id));
      }
    }
  },
  methods: {
    async handleSubmit() {
      try {
        if (this.isEdit) {
          await quizStore.update(this.$route.params.id, this.formData);
        } else {
          await quizStore.create(this.formData);
        }
        router.push('/admin/quizzes');
      } catch (error) {
        console.error(error);
        this.errorMessage = 'An error occurred while submitting the form.';
      }
    },
  },
};
</script>
