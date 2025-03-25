import { get, post, put, del } from '@/utils/fetchHelper';
import { reactive } from 'vue';
import { questionStore } from '.';

const store = reactive({
  quizzes: new Map(),

  _setQuiz(quiz) {
    if (this.quizzes.has(quiz.id)) {
      Object.assign(this.quizzes.get(quiz.id), quiz);
    } else {
      this.quizzes.set(quiz.id, quiz);
    }
    return this.quizzes.get(quiz.id);
  },

  async fetch(id) {
    id = parseInt(id);
    const { quiz } = await get(`/api/quiz/get/${id}`);
    return this._setQuiz(quiz);
  },

  async fetchAll() {
    const { quizzes } = await get('/api/quiz/get-all');
    quizzes.forEach(quiz => this._setQuiz(quiz));
    return this.quizzes;
  },

  async create(data) {
    const { quiz } = await post('/api/quiz/create', data);
    return this._setQuiz(quiz);
  },

  async update(id, data) {
    id = parseInt(id);
    const { quiz } = await put(`/api/quiz/update/${id}`, data);
    Object.assign(this.quizzes.get(id), quiz);
  },

  async delete(id) {
    id = parseInt(id);
    await del(`/api/quiz/delete/${id}`);
    this.quizzes.delete(id);
  },

  getQuestionsForQuiz(quiz) {
    return quiz.questions
      .map(questionId => questionStore.questions.get(questionId))
      .filter(question => question !== undefined);
  },
});

export default store;
