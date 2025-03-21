<template>
  <div class="container mt-4">
    <h1 class="text-primary fw-bold mb-4">Edit Chapter</h1>
    <AdminChapterForm
      v-if="chapter"
      :isEdit="true"
      :initialData="chapter"
      :subjectId="chapter.subject_id"
    />
  </div>
</template>

<script>
import AdminChapterForm from '@/components/AdminChapterForm.vue';
import { get } from '@/utils/fetchHelper';

export default {
  components: {
    AdminChapterForm,
  },
  data() {
    return {
      chapter: null,
    };
  },
  async created() {
    try {
      const result = await get(`/api/admin/get-chapter/${this.$route.params.id}`);
      if (result.success) {
        this.chapter = result.chapter;
      }
    } catch (error) {
      console.error('Failed to fetch chapter:', error);
    }
  },
};
</script>
