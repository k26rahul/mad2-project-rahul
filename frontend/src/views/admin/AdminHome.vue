<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="text-primary fw-bold">Subjects & Chapters</h1>
      <router-link to="/admin/new-subject" class="btn btn-primary shadow-sm">
        <i class="bi bi-plus-lg fs-5"></i> Add Subject
      </router-link>
    </div>

    <!-- No subjects message -->
    <div v-if="subjects.length === 0" class="text-center p-5">
      <h3 class="text-muted">No subjects found</h3>
      <p class="lead">Start by adding a new subject</p>
    </div>

    <!-- Subjects grid -->
    <div class="row g-4 mb-4">
      <div v-for="subject in subjects" :key="subject.id" class="col-md-6">
        <div class="card border-0 shadow-lg rounded-4 h-100">
          <!-- Subject header -->
          <div class="card-header bg-primary bg-opacity-10 border-0 rounded-top-4">
            <div class="d-flex justify-content-between align-items-center">
              <h3 class="fw-bold mb-0">{{ subject.name }}</h3>
              <div class="btn-group">
                <button @click="editSubject(subject.id)" class="btn btn-sm btn-outline-primary">
                  <i class="bi bi-pencil fs-5"></i>
                </button>
                <button @click="deleteSubject(subject.id)" class="btn btn-sm btn-outline-danger">
                  <i class="bi bi-trash fs-5"></i>
                </button>
              </div>
            </div>
            <p class="text-muted mb-0">{{ subject.description }}</p>
          </div>

          <!-- Chapters list -->
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h4 class="text-secondary fw-semibold">Chapters</h4>
              <router-link
                :to="`/admin/new-chapter/${subject.id}`"
                class="btn btn-sm btn-outline-primary"
              >
                <i class="bi bi-plus-lg fs-5"></i> Add Chapter
              </router-link>
            </div>

            <!-- No chapters message -->
            <div v-if="!subject.chapters?.length" class="text-center p-3">
              <p class="text-muted mb-0">No chapters yet</p>
            </div>

            <!-- Chapters -->
            <div v-else class="list-group list-group-flush">
              <div
                v-for="chapter in subject.chapters"
                :key="chapter.id"
                class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
              >
                <div>
                  <h5 class="mb-1">{{ chapter.name }}</h5>
                  <p class="text-muted small mb-0">{{ chapter.description }}</p>
                </div>
                <div class="btn-group">
                  <button @click="editChapter(chapter.id)" class="btn btn-sm btn-outline-secondary">
                    <i class="bi bi-pencil fs-5"></i>
                  </button>
                  <button @click="deleteChapter(chapter.id)" class="btn btn-sm btn-outline-danger">
                    <i class="bi bi-trash fs-5"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { get } from '@/utils/fetchHelper';

export default {
  data() {
    return {
      subjects: [],
    };
  },
  async created() {
    try {
      const result = await get('/api/admin/subjects');
      if (result.success) {
        this.subjects = result.subjects;
      }
    } catch (error) {
      console.error('Failed to fetch subjects:', error);
    }
  },
  methods: {
    editSubject(id) {
      this.$router.push(`/admin/edit-subject/${id}`);
    },
    deleteSubject(id) {
      console.log('Delete subject:', id);
    },
    editChapter(id) {
      this.$router.push(`/admin/edit-chapter/${id}`);
    },
    deleteChapter(id) {
      console.log('Delete chapter:', id);
    },
  },
};
</script>
