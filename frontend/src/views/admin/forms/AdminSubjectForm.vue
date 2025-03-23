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
import store from '@/store';
import router from '@/router';

export default {
  data() {
    return {
      formData: {
        name: '',
        description: '',
      },
      errorMessage: '',
      isEdit: false,
    };
  },
  async created() {
    const id = this.$route.params.id;
    if (id) {
      this.isEdit = true;
      try {
        const result = await store.subjects.get(id);
        if (result.success) {
          this.formData = {
            name: result.subject.name,
            description: result.subject.description,
          };
        } else {
          this.errorMessage = result.message;
        }
      } catch (error) {
        this.errorMessage = 'Failed to fetch subject data';
      }
    }
  },
  methods: {
    async handleSubmit() {
      try {
        let result;
        if (this.isEdit) {
          result = await store.subjects.update(this.$route.params.id, this.formData);
        } else {
          result = await store.subjects.create(this.formData);
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
