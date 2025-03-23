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
      <router-link to="/admin/subject/new" class="btn btn-primary shadow-sm">
        <i class="bi bi-plus-lg fs-5"></i> Add Subject
      </router-link>
    </div>

    <!-- No results message -->
    <div v-if="subjects.filter(s => s.$matches).length === 0" class="text-center p-5">
      <h3 class="text-muted">No subjects found</h3>
      <p class="lead" v-if="subjects.length === 0">Start by adding a new subject</p>
    </div>

    <!-- Subjects grid -->
    <div class="row g-4 mb-4">
      <div v-for="subject in subjects.filter(s => s.$matches)" :key="subject.id" class="col-md-6">
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
                :to="`/admin/subject/${subject.id}/chapter/new`"
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
                v-for="chapter in subject.chapters.filter(c => c.$matches)"
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
import { subjectStore } from '@/store';
import { matchQuery } from '@/utils/searchUtil';

export default {
  data() {
    return {
      searchQuery: '',
      searchType: 'subject',
    };
  },

  computed: {
    subjects() {
      return subjectStore.subjects;
    },
  },

  watch: {
    searchQuery() {
      this.updateSearchMatches();
    },
    searchType() {
      this.updateSearchMatches();
    },
  },

  async created() {
    await subjectStore.init();
  },

  methods: {
    updateSearchMatches() {
      if (!this.searchQuery) {
        // If no search query, everything matches
        this.subjects.forEach(subject => {
          subject.$matches = true;
          if (subject.chapters) {
            subject.chapters.forEach(chapter => (chapter.$matches = true));
          }
        });
        return;
      }

      if (this.searchType === 'subject') {
        this.subjects.forEach(subject => {
          subject.$matches =
            matchQuery(subject.name, this.searchQuery) ||
            matchQuery(subject.description, this.searchQuery);
          if (subject.chapters) {
            subject.chapters.forEach(chapter => (chapter.$matches = true));
          }
        });
      } else {
        this.subjects.forEach(subject => {
          if (subject.chapters) {
            subject.chapters.forEach(chapter => {
              chapter.$matches =
                matchQuery(chapter.name, this.searchQuery) ||
                matchQuery(chapter.description, this.searchQuery);
            });
            // Subject matches if it has any matching chapters
            subject.$matches = subject.chapters.some(chapter => chapter.$matches);
          } else {
            subject.$matches = false;
          }
        });
      }
    },

    async editSubject(id) {
      this.$router.push(`/admin/subject/${id}/edit`);
    },

    async deleteSubject(id) {
      if (!confirm('Are you sure you want to delete this subject and all its chapters?')) return;
      await subjectStore.delete(id);
    },

    editChapter(id) {
      this.$router.push(`/admin/chapter/${id}/edit`);
    },

    async deleteChapter(id) {
      if (!confirm('Are you sure you want to delete this chapter?')) return;
      await store.chapters.delete(id);
    },
  },
};
</script>
