<template>
  <div class="container mt-4">
    <h1 class="text-primary fw-bold mb-4">Create New Chapter</h1>
    <AdminChapterForm :isEdit="false" :subjectId="$route.params.subject_id" />
  </div>
</template>

<script>
import AdminChapterForm from '@/components/AdminChapterForm.vue';

export default {
  components: {
    AdminChapterForm,
  },
};
</script>
