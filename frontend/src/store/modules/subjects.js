import { get, post, put, del } from '@/utils/fetchHelper';

export default {
  state: {
    subjects: [],
  },

  async fetchAll() {
    const result = await get('/api/subject/get-all');
    if (result.success) {
      this.state.subjects = result.subjects;
    }
    return result;
  },

  async create(data) {
    const result = await post('/api/subject/create', data);
    if (result.success) {
      await this.fetchAll();
    }
    return result;
  },

  async update(id, data) {
    const result = await put(`/api/subject/update/${id}`, data);
    if (result.success) {
      await this.fetchAll();
    }
    return result;
  },

  async delete(id) {
    const result = await del(`/api/subject/delete/${id}`);
    if (result.success) {
      await this.fetchAll();
    }
    return result;
  },

  async get(id) {
    const result = await get(`/api/subject/get/${id}`);
    return result;
  },
};
