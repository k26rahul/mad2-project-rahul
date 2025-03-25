import { get, post, put, del } from '@/utils/fetchHelper';
import { reactive } from 'vue';
import { subjectStore, quizStore } from '.';

const store = reactive({
  chapters: new Map(),

  _setChapter(chapter) {
    if (this.chapters.has(chapter.id)) {
      Object.assign(this.chapters.get(chapter.id), chapter);
    } else {
      this.chapters.set(chapter.id, chapter);
    }
    return this.chapters.get(chapter.id);
  },

  async fetch(id) {
    id = parseInt(id);
    const { chapter } = await get(`/api/chapter/get/${id}`);
    return this._setChapter(chapter);
  },

  async fetchAll() {
    const { chapters } = await get('/api/chapter/get-all');
    const validIds = new Set(chapters.map(chapter => chapter.id));
    chapters.forEach(chapter => this._setChapter(chapter));
    for (const id of this.chapters.keys()) {
      if (!validIds.has(id)) {
        this.chapters.delete(id);
      }
    }
    return this.chapters;
  },

  async create(data) {
    const { chapter } = await post('/api/chapter/create', data);
    this._setChapter(chapter);
    subjectStore.handleChapterCreated(chapter);
  },

  async update(id, data) {
    id = parseInt(id);
    const { chapter } = await put(`/api/chapter/update/${id}`, data);
    this._setChapter(chapter);
  },

  async delete(id) {
    id = parseInt(id);
    const chapter = this.chapters.get(id);
    await del(`/api/chapter/delete/${id}`);
    subjectStore.handleChapterDeleted(chapter);
    quizStore.handleChapterDeleted();
    this.chapters.delete(id);
  },

  handleSubjectDeleted() {
    this.fetchAll();
    quizStore.handleChapterDeleted();
  },
});

export default store;
