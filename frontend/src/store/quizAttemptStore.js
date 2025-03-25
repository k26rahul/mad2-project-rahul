import { get, post } from '@/utils/fetchHelper';
import { reactive, watch } from 'vue';

const STORAGE_KEY = 'quiz-answer-feedbacks';

const store = reactive({
  attempts: new Map(),
  answerFeedbacks: new Map(),

  _setAttempt(attempt) {
    this.attempts.set(attempt.id, attempt);
    return attempt;
  },

  _setAnswerFeedback(attemptId, feedback) {
    this.answerFeedbacks.set(attemptId, feedback);
    return this.answerFeedbacks.get(attemptId);
  },

  async fetchAll() {
    const { attempts } = await get('/api/user/quiz-attempts');
    attempts.forEach(attempt => this._setAttempt(attempt));

    // Restore answer feedbacks from localStorage
    try {
      const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
      Object.entries(stored).forEach(([id, feedback]) => {
        this.answerFeedbacks.set(parseInt(id), feedback);
      });
    } catch (e) {
      console.warn('Failed to restore answer feedbacks from localStorage');
    }

    return this.attempts;
  },

  async create(quizId, answers) {
    const response = await post(`/api/user/quiz-attempts/${quizId}`, { answers });
    const { attempt, answer_feedback } = response;

    this._setAttempt(attempt);
    this._setAnswerFeedback(attempt.id, answer_feedback);

    return {
      attempt: this.attempts.get(attempt.id),
      answerFeedback: this.answerFeedbacks.get(attempt.id),
    };
  },
});

// Watch answerFeedbacks changes and persist to localStorage
watch(
  () => Array.from(store.answerFeedbacks.entries()),
  entries => {
    const stored = Object.fromEntries(entries);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(stored));
  },
  { deep: true }
);

export default store;

// This store is specifically designed for the user dashboard to manage quiz attempts
// Since users cannot create/delete subjects/chapters/questions/quizzes,
// no handle methods for related object changes are needed

/*
Data Structure:

attempts: Map<number, {
  id: number,
  attempted_at: string,
  chapter_name: string,
  correct_questions: number,
  incorrect_questions: number,
  percentage: number,
  quiz_id: number,
  quiz_title: string,
  score: number,
  subject_name: string,
  total_questions: number,
  user_id: number
}>

answerFeedbacks: Map<number, {
  [questionId: string]: {
    correct: boolean,
    submitted: number
  }
}>
*/
