import { get, post, put, del } from '@/utils/fetchHelper';
import { reactive } from 'vue';

export default reactive({
  chapters: [],
  initialized: false,

  async init() {
    if (!this.initialized) {
      await this.fetchAll();
      this.initialized = true;
    }
  },

  async fetchAll() {
    const result = await get('/api/chapter/get-all');
    if (result.success) {
      this.chapters = result.chapters;
    }
    return result;
  },

  async create(data) {
    const result = await post('/api/chapter/create', data);
    if (result.success) {
      await this.store.subjects.fetchAll();
    }
    return result;
  },

  async update(id, data) {
    const result = await put(`/api/chapter/update/${id}`, data);
    if (result.success) {
      await this.store.subjects.fetchAll();
    }
    return result;
  },

  async delete(id) {
    const result = await del(`/api/chapter/delete/${id}`);
    if (result.success) {
      await this.store.subjects.fetchAll();
    }
    return result;
  },

  async get(id) {
    const result = await get(`/api/chapter/get/${id}`);
    return result;
  },
});
