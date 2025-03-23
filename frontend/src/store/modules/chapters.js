import { get, post, put, del } from '@/utils/fetchHelper';

export default {
  state: {
    chapters: [],
  },

  async fetchAll() {
    // This might not be needed as chapters come with subjects
    const result = await get('/api/chapter/get-all');
    if (result.success) {
      this.state.chapters = result.chapters;
    }
    return result;
  },

  async create(data) {
    const result = await post('/api/chapter/create', data);
    if (result.success) {
      // Refresh subjects as chapters are nested in subjects
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
};
