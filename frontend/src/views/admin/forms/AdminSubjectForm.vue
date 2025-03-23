<template>
  <div class="container p-4 border-0 shadow-lg rounded-4 bg-white" style="max-width: 600px">
    <h1 class="text-center mb-4">{{ isEdit ? 'Edit Subject' : 'Create New Subject' }}</h1>
    <form @submit.prevent="handleSubmit">
      <div class="mb-3">
        <label for="name" class="form-label fw-semibold">Subject Name</label>
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
        {{ isEdit ? 'Update Subject' : 'Create Subject' }}
      </button>
    </form>
  </div>
</template>

<script>
import { subjectStore } from '@/store';
import router from '@/router';

export default {
  data() {
    return {
      formData: {
        name: '',
        description: '',
      },
      errorMessage: '',
    };
  },

  computed: {
    isEdit() {
      return this.$route.name === 'AdminSubjectEdit';
    },
  },

  async created() {
    if (this.isEdit) {
      const id = this.$route.params.id;
      const subject = subjectStore.subjects.get(parseInt(id));
      if (subject) {
        this.formData = {
          name: subject.name,
          description: subject.description,
        };
      }
    }
  },

  methods: {
    async handleSubmit() {
      try {
        if (this.isEdit) {
          await subjectStore.update(this.$route.params.id, this.formData);
        } else {
          await subjectStore.create(this.formData);
        }
        router.push('/admin/home');
      } catch (error) {
        this.errorMessage = 'An error occurred while processing your request.';
      }
    },
  },
};
</script>
