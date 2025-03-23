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
import store from '@/store/store/store';
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
      isEdit: false,
    };
  },

  computed: {
    subjects() {
      return store.subjects;
    },
    chapters() {
      return this.selectedSubject ? this.selectedSubject.chapters || [] : [];
    },
  },

  async created() {
    await store.subjects.fetchAll();
    const id = this.$route.params.id;
    if (id) {
      this.isEdit = true;
      await this.loadQuizData(id);
    }
  },

  methods: {
    async loadQuizData(id) {
      try {
        const result = await store.quizzes.get(id);
        if (result.success) {
          const formattedDate = result.quiz.start_time
            ? new Date(result.quiz.start_time).toISOString().slice(0, 16)
            : '';

          this.formData = {
            title: result.quiz.title,
            description: result.quiz.description,
            chapter_id: result.quiz.chapter_id,
            start_time: formattedDate,
            duration: result.quiz.duration,
          };

          this.selectedSubject = this.subjects.find(s =>
            s.chapters.some(c => c.id === result.quiz.chapter_id)
          );
        }
      } catch (error) {
        this.errorMessage = 'Failed to load quiz data';
      }
    },

    async handleSubmit() {
      try {
        let result;
        if (this.isEdit) {
          result = await store.quizzes.update(this.$route.params.id, this.formData);
        } else {
          result = await store.quizzes.create(this.formData);
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
