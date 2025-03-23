import { get, post, put, del } from '@/utils/fetchHelper';
import { reactive } from 'vue';

export default reactive({
  subjects: {},
  initialFetchCompleted: false,

  async initialFetchAll() {
    if (!this.initialFetchCompleted) {
      await this.fetchAll();
      this.initialFetchCompleted = true;
    }
  },

  async fetch(id) {
    const result = await get(`/api/subject/get/${id}`);
    this.subjects[id] = result.subject;
  },

  async fetchAll() {
    const result = await get('/api/subject/get-all');
    this.subjects = {};
    result.subjects.forEach(subject => {
      this.subjects[subject.id] = subject;
    });
  },

  async create(data) {
    const result = await post('/api/subject/create', data);
    this.subjects[result.subject.id] = result.subject;
  },

  async update(id, data) {
    const result = await put(`/api/subject/update/${id}`, data);
    this.subjects[id] = result.subject;
  },

  async delete(id) {
    const result = await del(`/api/subject/delete/${id}`);
    delete this.subjects[id];
  },
});
