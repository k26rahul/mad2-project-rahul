<template>
  <div class="container p-4 border-0 shadow-lg rounded-4 bg-white" style="max-width: 600px">
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
import { post, put } from '@/utils/fetchHelper';
import router from '@/router';

export default {
  props: {
    isEdit: {
      type: Boolean,
      default: false,
    },
    initialData: {
      type: Object,
      default: () => ({}),
    },
    subjectId: {
      type: [Number, String],
      required: true,
    },
  },
  data() {
    return {
      formData: {
        name: '',
        description: '',
      },
      errorMessage: '',
    };
  },
  created() {
    if (this.isEdit && this.initialData) {
      this.formData = { ...this.initialData };
    }
  },
  methods: {
    async handleSubmit() {
      try {
        let result;
        if (this.isEdit) {
          result = await put(`/api/admin/chapters/${this.initialData.id}`, this.formData);
        } else {
          result = await post('/api/admin/chapters', {
            ...this.formData,
            subject_id: this.subjectId,
          });
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
