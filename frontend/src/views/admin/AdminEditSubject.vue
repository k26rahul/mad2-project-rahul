<template>
  <div class="container mt-4">
    <h1 class="text-primary fw-bold mb-4">Edit Subject</h1>
    <AdminSubjectForm v-if="subject" :isEdit="true" :initialData="subject" />
  </div>
</template>

<script>
import AdminSubjectForm from '@/components/AdminSubjectForm.vue';
import { get } from '@/utils/fetchHelper';

export default {
  components: {
    AdminSubjectForm,
  },
  data() {
    return {
      subject: null,
    };
  },
  async created() {
    try {
      const result = await get(`/api/admin/get-subject/${this.$route.params.id}`);
      if (result.success) {
        this.subject = result.subject;
      }
    } catch (error) {
      console.error('Failed to fetch subject:', error);
    }
  },
};
</script>
