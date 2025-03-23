import { get, post, put, del } from '@/utils/fetchHelper';
import { reactive } from 'vue';

export default reactive({
  questions: {},
  initialFetchCompleted: false,

  async initialFetchAll() {
    if (!this.initialFetchCompleted) {
      await this.fetchAll();
      this.initialFetchCompleted = true;
    }
  },

  async fetch(id) {
    const result = await get(`/api/question/get/${id}`);
    this.questions[id] = result.question;
  },

  async fetchAll() {
    const result = await get('/api/question/get-all');
    this.questions = {};
    result.questions.forEach(question => {
      this.questions[question.id] = question;
    });
  },

  async create(data) {
    const result = await post('/api/question/create', data);
    this.questions[result.question.id] = result.question;
  },

  async update(id, data) {
    const result = await put(`/api/question/update/${id}`, data);
    this.questions[id] = result.question;
  },

  async delete(id) {
    await del(`/api/question/delete/${id}`);
    delete this.questions[id];
  },
});
