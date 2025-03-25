import { get, post, put, del } from '@/utils/fetchHelper';
import { reactive } from 'vue';
import { chapterStore } from '.';

const store = reactive({
  subjects: new Map(),

  _setSubject(subject) {
    if (this.subjects.has(subject.id)) {
      Object.assign(this.subjects.get(subject.id), subject);
    } else {
      this.subjects.set(subject.id, subject);
    }
    return this.subjects.get(subject.id);
  },

  async fetch(id) {
    id = parseInt(id);
    const { subject } = await get(`/api/subject/get/${id}`);
    return this._setSubject(subject);
  },

  async fetchAll() {
    const { subjects } = await get('/api/subject/get-all');
    subjects.forEach(subject => this._setSubject(subject));
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
    id = parseInt(id);
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
