import { get, post, put, del } from '@/utils/fetchHelper';
import { reactive } from 'vue';

export default reactive({
  chapters: {},
  initialFetchCompleted: false,

  async initialFetchAll() {
    if (!this.initialFetchCompleted) {
      await this.fetchAll();
      this.initialFetchCompleted = true;
    }
  },

  async fetch(id) {
    const result = await get(`/api/chapter/get/${id}`);
    this.chapters[id] = result.chapter;
  },

  async fetchAll() {
    const result = await get('/api/chapter/get-all');
    this.chapters = {};
    result.chapters.forEach(chapter => {
      this.chapters[chapter.id] = chapter;
    });
  },

  async create(data) {
    const result = await post('/api/chapter/create', data);
    this.chapters[result.chapter.id] = result.chapter;
  },

  async update(id, data) {
    const result = await put(`/api/chapter/update/${id}`, data);
    this.chapters[id] = result.chapter;
  },

  async delete(id) {
    await del(`/api/chapter/delete/${id}`);
    delete this.chapters[id];
  },
});
