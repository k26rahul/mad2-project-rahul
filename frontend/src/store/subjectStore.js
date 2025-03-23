import { get, post, put, del } from '@/utils/fetchHelper';
import { reactive } from 'vue';
import chapterStore from './chapterStore';

const store = reactive({
  subjects: new Map(),

  async fetch(id) {
    id = parseInt(id);
    const { subject } = await get(`/api/subject/get/${id}`);
    if (this.subjects.has(id)) {
      Object.assign(this.subjects.get(id), subject);
    } else {
      this.subjects.set(id, subject);
    }
    return this.subjects.get(id);
  },

  async fetchAll() {
    const { subjects } = await get('/api/subject/get-all');
    subjects.forEach(subject => {
      if (this.subjects.has(subject.id)) {
        Object.assign(this.subjects.get(subject.id), subject);
      } else {
        this.subjects.set(subject.id, subject);
      }
    });
    return this.subjects;
  },

  async create(data) {
    const { subject } = await post('/api/subject/create', data);
    this.subjects.set(subject.id, subject);
  },

  async update(id, data) {
    id = parseInt(id);
    const { subject } = await put(`/api/subject/update/${id}`, data);
    Object.assign(this.subjects.get(id), subject);
  },

  async delete(id) {
    await del(`/api/subject/delete/${id}`);
    this.subjects.delete(id);
  },

  getChaptersForSubject(subject) {
    return subject.chapters
      .map(chapterId => chapterStore.chapters.get(chapterId))
      .filter(chapter => chapter !== undefined);
  },
});

export default store;
