import { get, post, put, del } from '@/utils/fetchHelper';
import { reactive } from 'vue';

export default reactive({
  quizzes: {},
  initialFetchCompleted: false,

  async initialFetchAll() {
    if (!this.initialFetchCompleted) {
      await this.fetchAll();
      this.initialFetchCompleted = true;
    }
  },

  async fetch(id) {
    const result = await get(`/api/quiz/get/${id}`);
    this.quizzes[id] = result.quiz;
  },

  async fetchAll() {
    const result = await get('/api/quiz/get-all');
    this.quizzes = {};
    result.quizzes.forEach(quiz => {
      this.quizzes[quiz.id] = quiz;
    });
  },

  async create(data) {
    const result = await post('/api/quiz/create', data);
    this.quizzes[result.quiz.id] = result.quiz;
  },

  async update(id, data) {
    const result = await put(`/api/quiz/update/${id}`, data);
    this.quizzes[id] = result.quiz;
  },

  async delete(id) {
    await del(`/api/quiz/delete/${id}`);
    delete this.quizzes[id];
  },
});
