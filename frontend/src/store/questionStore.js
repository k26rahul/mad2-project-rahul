import { get, post, put, del } from '@/utils/fetchHelper';
import { reactive } from 'vue';
import { quizStore } from '@/store';

const store = reactive({
  questions: new Map(),

  async fetch(id) {
    id = parseInt(id);
    const { question } = await get(`/api/question/get/${id}`);
    if (this.questions.has(id)) {
      Object.assign(this.questions.get(id), question);
    } else {
      this.questions.set(id, question);
    }
    return this.questions.get(id);
  },

  async fetchAll() {
    const { questions } = await get('/api/question/get-all');
    questions.forEach(question => {
      if (this.questions.has(question.id)) {
        Object.assign(this.questions.get(question.id), question);
      } else {
        this.questions.set(question.id, question);
      }
    });
    return this.questions;
  },

  async create(data) {
    const { question } = await post('/api/question/create', data);
    this.questions.set(question.id, question);
    quizStore.fetch(question.quiz_id);
  },

  async update(id, data) {
    id = parseInt(id);
    const { question } = await put(`/api/question/update/${id}`, data);
    Object.assign(this.questions.get(id), question);
  },

  async delete(id) {
    await del(`/api/question/delete/${id}`);
    this.questions.delete(id);
  },
});

export default store;
