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
      const result = await get('/api/admin/subjects');
      if (result.success) {
        const chapterId = parseInt(this.$route.params.id);
        for (const subject of result.subjects) {
          const chapter = subject.chapters.find(c => c.id === chapterId);
          if (chapter) {
            this.chapter = chapter;
            break;
          }
        }
      }
    } catch (error) {
      console.error('Failed to fetch chapter:', error);
    }
  },
};
</script>
