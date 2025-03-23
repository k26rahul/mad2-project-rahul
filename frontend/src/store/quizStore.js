import { get, post, put, del } from '@/utils/fetchHelper';
import { reactive } from 'vue';
import questionStore from './questionStore';

const store = reactive({
  quizzes: new Map(),

  async fetch(id) {
    id = parseInt(id);
    const { quiz } = await get(`/api/quiz/get/${id}`);
    if (this.quizzes.has(id)) {
      Object.assign(this.quizzes.get(id), quiz);
    } else {
      this.quizzes.set(id, quiz);
    }
    return this.quizzes.get(id);
  },

  async fetchAll() {
    const { quizzes } = await get('/api/quiz/get-all');
    quizzes.forEach(quiz => {
      if (this.quizzes.has(quiz.id)) {
        Object.assign(this.quizzes.get(quiz.id), quiz);
      } else {
        this.quizzes.set(quiz.id, quiz);
      }
    });
    return this.quizzes;
  },

  async create(data) {
    const { quiz } = await post('/api/quiz/create', data);
    this.quizzes.set(quiz.id, quiz);
  },

  async update(id, data) {
    id = parseInt(id);
    const { quiz } = await put(`/api/quiz/update/${id}`, data);
    Object.assign(this.quizzes.get(id), quiz);
  },

  async delete(id) {
    await del(`/api/quiz/delete/${id}`);
    this.quizzes.delete(id);
  },

  getQuestionsForQuiz(quiz) {
    return quiz.questions.map(qId => questionStore.questions.get(qId)).filter(q => q !== undefined);
  },
});

export default store;
