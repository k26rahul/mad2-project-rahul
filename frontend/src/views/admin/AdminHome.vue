<template>
  <div class="container mt-4">
    <!-- Search Controls -->
    <div class="row mb-4">
      <div class="col-md-8">
        <div class="input-group">
          <select v-model="searchType" class="form-select flex-grow-0" style="width: 140px">
            <option value="subject">Search Subjects</option>
            <option value="chapter">Search Chapters</option>
          </select>
          <input
            type="text"
            v-model="searchQuery"
            class="form-control"
            :placeholder="searchType === 'subject' ? 'Search subjects...' : 'Search chapters...'"
          />
        </div>
      </div>
    </div>

    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="text-primary fw-bold">Subjects & Chapters</h1>
      <router-link to="/admin/new-subject" class="btn btn-primary shadow-sm">
        <i class="bi bi-plus-lg fs-5"></i> Add Subject
      </router-link>
    </div>

    <!-- No results message -->
    <div v-if="subjects.filter(s => subjectPass(s)).length === 0" class="text-center p-5">
      <h3 class="text-muted">No subjects found</h3>
      <p class="lead" v-if="subjects.length === 0">Start by adding a new subject</p>
    </div>

    <!-- Subjects grid -->
    <div class="row g-4 mb-4">
      <div
        v-for="subject in subjects.filter(s => subjectPass(s))"
        :key="subject.id"
        class="col-md-6"
      >
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
            <div v-if="!(subject.chapters && subject.chapters.length)" class="text-center p-3">
              <p class="text-muted mb-0">No chapters yet</p>
            </div>

            <!-- Chapters -->
            <div v-else class="list-group list-group-flush">
              <div
                v-for="chapter in searchType === 'subject'
                  ? subject.chapters
                  : subject.chapters.filter(c => chapterPass(c))"
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
                <!-- End of chapter buttons/actions -->
              </div>
              <!-- End of chapter list item -->
            </div>
            <!-- End of chapters list -->
          </div>
          <!-- End of card-body -->
        </div>
        <!-- End of subject card -->
      </div>
      <!-- End of subject column -->
    </div>
    <!-- End of subjects grid -->
  </div>
  <!-- End of container -->
</template>

<script>
import { get, del } from '@/utils/fetchHelper';
import { matchQuery } from '@/utils/searchUtil';

export default {
  data() {
    return {
      subjects: [],
      searchQuery: '',
      searchType: 'subject',
    };
  },

  async created() {
    await this.fetchSubjects();
  },

  methods: {
    subjectPass(subject) {
      if (!this.searchQuery) return true;
      if (this.searchType === 'subject') {
        return (
          matchQuery(subject.name, this.searchQuery) ||
          (subject.description && matchQuery(subject.description, this.searchQuery))
        );
      }
      return (
        subject.chapters &&
        subject.chapters.some(
          chapter =>
            matchQuery(chapter.name, this.searchQuery) ||
            (chapter.description && matchQuery(chapter.description, this.searchQuery))
        )
      );
    },

    chapterPass(chapter) {
      if (!this.searchQuery) return true;
      return (
        matchQuery(chapter.name, this.searchQuery) ||
        (chapter.description && matchQuery(chapter.description, this.searchQuery))
      );
    },

    async fetchSubjects() {
      try {
        const result = await get('/api/subject/get-all');
        if (result.success) {
          this.subjects = result.subjects;
        }
      } catch (error) {
        console.error('Failed to fetch subjects:', error);
      }
    },

    editSubject(id) {
      this.$router.push(`/admin/edit-subject/${id}`);
    },

    async deleteSubject(id) {
      if (!confirm('Are you sure you want to delete this subject and all its chapters?')) return;

      try {
        const result = await del(`/api/subject/delete/${id}`);
        if (result.success) await this.fetchSubjects();
      } catch (error) {
        console.error('Failed to delete subject:', error);
      }
    },

    editChapter(id) {
      this.$router.push(`/admin/edit-chapter/${id}`);
    },

    async deleteChapter(id) {
      if (!confirm('Are you sure you want to delete this chapter?')) return;

      try {
        const result = await del(`/api/chapter/delete/${id}`);
        if (result.success) await this.fetchSubjects();
      } catch (error) {
        console.error('Failed to delete chapter:', error);
      }
    },
  },
};
</script>
