import { get, post, put, del } from '@/utils/fetchHelper';
import { reactive } from 'vue';
import { subjectStore } from '.';

const store = reactive({
  chapters: new Map(),

  async fetch(id) {
    id = parseInt(id);
    const { chapter } = await get(`/api/chapter/get/${id}`);
    if (this.chapters.has(id)) {
      Object.assign(this.chapters.get(id), chapter);
    } else {
      this.chapters.set(id, chapter);
    }
    return this.chapters.get(id);
  },

  async fetchAll() {
    const { chapters } = await get('/api/chapter/get-all');
    chapters.forEach(chapter => {
      if (this.chapters.has(chapter.id)) {
        Object.assign(this.chapters.get(chapter.id), chapter);
      } else {
        this.chapters.set(chapter.id, chapter);
      }
    });
    return this.chapters;
  },

  async create(data) {
    const { chapter } = await post('/api/chapter/create', data);
    this.chapters.set(chapter.id, chapter);
    subjectStore.fetch(chapter.subject_id);
  },

  async update(id, data) {
    id = parseInt(id);
    const { chapter } = await put(`/api/chapter/update/${id}`, data);
    Object.assign(this.chapters.get(id), chapter);
  },

  async delete(id) {
    id = parseInt(id);
    await del(`/api/chapter/delete/${id}`);
    subjectStore.fetch(this.chapters.get(id).subject_id);
    this.chapters.delete(id);
  },
});

export default store;
