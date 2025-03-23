import { get, post, put, del } from '@/utils/fetchHelper';
import { reactive } from 'vue';

export default reactive({
  questions: [],
  initialized: false,

  async init() {
    if (!this.initialized) {
      await this.fetchAll();
      this.initialized = true;
    }
  },

  async fetchAll() {
    const result = await get('/api/question/get-all');
    if (result.success) {
      this.questions = result.questions;
    }
    return result;
  },
  async get(id) {
    const result = await get(`/api/question/get/${id}`);
    return result;
  },
  async create(data) {
    const result = await post('/api/question/create', data);
    if (result.success) {
      await this.store.quizzes.fetchAll();
    }
    return result;
  },
  async update(id, data) {
    const result = await put(`/api/question/update/${id}`, data);
    if (result.success) {
      await this.store.quizzes.fetchAll();
    }
    return result;
  },
  async delete(id) {
    const result = await del(`/api/question/delete/${id}`);
    if (result.success) {
      await this.store.quizzes.fetchAll();
    }
    return result;
  },
});
