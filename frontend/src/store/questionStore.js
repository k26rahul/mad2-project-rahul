import { get, post, put, del } from '@/utils/fetchHelper';
import { reactive } from 'vue';
import { quizStore } from '.';

const store = reactive({
  questions: new Map(),

  _setQuestion(question) {
    if (this.questions.has(question.id)) {
      Object.assign(this.questions.get(question.id), question);
    } else {
      this.questions.set(question.id, question);
    }
    return this.questions.get(question.id);
  },

  async fetch(id) {
    id = parseInt(id);
    const { question } = await get(`/api/question/get/${id}`);
    return this._setQuestion(question);
  },

  async fetchAll() {
    const { questions } = await get('/api/question/get-all');
    const validIds = new Set(questions.map(question => question.id));
    questions.forEach(question => this._setQuestion(question));
    for (const id of this.questions.keys()) {
      if (!validIds.has(id)) {
        this.questions.delete(id);
      }
    }
    return this.questions;
  },

  async create(data) {
    const { question } = await post('/api/question/create', data);
    this._setQuestion(question);
    quizStore.handleQuestionCreated(question);
  },

  async update(id, data) {
    id = parseInt(id);
    const { question } = await put(`/api/question/update/${id}`, data);
    this._setQuestion(question);
  },

  async delete(id) {
    id = parseInt(id);
    const question = this.questions.get(id);
    await del(`/api/question/delete/${id}`);
    quizStore.handleQuestionDeleted(question);
    this.questions.delete(id);
  },

  handleQuizDeleted() {
    this.fetchAll();
  },
});

export default store;
