<template>
  <div class="container p-4 border-0 shadow-lg rounded-4 bg-white" style="max-width: 600px">
    <h1 class="text-center mb-4">{{ isEdit ? 'Edit Chapter' : 'Create New Chapter' }}</h1>
    <form @submit.prevent="handleSubmit">
      <div class="mb-3">
        <label for="name" class="form-label fw-semibold">Chapter Name</label>
        <input
          type="text"
          id="name"
          class="form-control shadow-sm"
          v-model="formData.name"
          required
        />
      </div>
      <div class="mb-3">
        <label for="description" class="form-label fw-semibold">Description</label>
        <textarea
          id="description"
          class="form-control shadow-sm"
          v-model="formData.description"
          rows="3"
        ></textarea>
      </div>
      <div v-if="errorMessage" class="alert alert-danger shadow-sm" role="alert">
        {{ errorMessage }}
      </div>
      <button type="submit" class="btn btn-primary w-100 shadow-sm">
        {{ isEdit ? 'Update Chapter' : 'Create Chapter' }}
      </button>
    </form>
  </div>
</template>

<script>
import chapterStore from '@/store/chapterStore';
import router from '@/router';

export default {
  data() {
    return {
      formData: {
        name: '',
        description: '',
        subject_id: null,
      },
      errorMessage: '',
    };
  },
  computed: {
    isEdit() {
      return this.$route.name === 'AdminChapterEdit';
    },
  },
  async created() {
    const subject_id = this.$route.params.subject_id;
    if (subject_id) {
      this.formData.subject_id = parseInt(subject_id);
    }

    if (this.isEdit) {
      const id = this.$route.params.id;
      const chapter = chapterStore.chapters.get(parseInt(id));
      if (chapter) {
        this.formData = {
          name: chapter.name,
          description: chapter.description,
          subject_id: chapter.subject_id,
        };
      }
    }
  },
  methods: {
    async handleSubmit() {
      try {
        if (this.isEdit) {
          await chapterStore.update(this.$route.params.id, this.formData);
        } else {
          await chapterStore.create(this.formData);
        }
        router.push('/admin/home');
      } catch (error) {
        this.errorMessage = 'An error occurred while submitting the form.';
      }
    },
  },
};
</script>
