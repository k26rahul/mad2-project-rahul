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
import { post, put, get } from '@/utils/fetchHelper';
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
      isEdit: false,
    };
  },
  async created() {
    const id = this.$route.params.id;
    const subject_id = this.$route.params.subject_id;

    if (id) {
      this.isEdit = true;
      try {
        const result = await get(`/api/chapter/get/${id}`);
        if (result.success) {
          this.formData = {
            name: result.chapter.name,
            description: result.chapter.description,
            subject_id: result.chapter.subject_id,
          };
        } else {
          this.errorMessage = result.message;
        }
      } catch (error) {
        this.errorMessage = 'Failed to fetch chapter data';
      }
    } else if (subject_id) {
      this.formData.subject_id = parseInt(subject_id);
    }
  },
  methods: {
    async handleSubmit() {
      try {
        let result;
        if (this.isEdit) {
          result = await put(`/api/chapter/update/${this.$route.params.id}`, this.formData);
        } else {
          result = await post('/api/chapter/create', this.formData);
        }

        if (result.success) {
          router.push('/admin/home');
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
