import { get, post, put, del } from '@/utils/fetchHelper';
import { reactive } from 'vue';

export default reactive({
  quizzes: [],
  initialized: false,

  async init() {
    if (!this.initialized) {
      await this.fetchAll();
      this.initialized = true;
    }
  },

  async fetchAll() {
    const result = await get('/api/quiz/get-all');
    if (result.success) {
      this.quizzes = result.quizzes;
    }
    return result;
  },
  async create(data) {
    const result = await post('/api/quiz/create', data);
    if (result.success) {
      await this.fetchAll();
    }
    return result;
  },
  async update(id, data) {
    const result = await put(`/api/quiz/update/${id}`, data);
    if (result.success) {
      await this.fetchAll();
    }
    return result;
  },
  async delete(id) {
    const result = await del(`/api/quiz/delete/${id}`);
    if (result.success) {
      await this.fetchAll();
    }
    return result;
  },
  async get(id) {
    const result = await get(`/api/quiz/get/${id}`);
    return result;
  },
});
