<template>
  <div class="container mt-4">
    <h1 class="text-primary fw-bold mb-4">Create New Subject</h1>
    <AdminSubjectForm :isEdit="false" />
  </div>
</template>

<script>
import AdminSubjectForm from '@/components/AdminSubjectForm.vue';

export default {
  components: {
    AdminSubjectForm,
  },
};
</script>
