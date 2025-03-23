import { reactive, watch } from 'vue';
import subjects from './modules/subjects';
import chapters from './modules/chapters';
import quizzes from './modules/quizzes';
import questions from './modules/questions';

const store = reactive({
  auth: {
    isLoggedIn: false,
    role: null,
  },

  api: {
    origin: 'http://127.0.0.1:5000',
  },

  // Modules
  subjects: subjects.state,
  chapters: chapters.state,
  quizzes: quizzes.state,
  questions: questions.state,

  // Methods from modules
  ...subjects,
  ...chapters,
  ...quizzes,
  ...questions,
});

// Initialize store reference in modules
[subjects, chapters, quizzes, questions].forEach(module => {
  module.store = store;
});

// Restore auth state from local storage
const authStateFromLocalStorage = JSON.parse(localStorage.getItem('authState'));
if (authStateFromLocalStorage) {
  store.auth = { ...store.auth, ...authStateFromLocalStorage };
}

// Watch auth changes
watch(
  () => store.auth,
  newAuthState => {
    localStorage.setItem('authState', JSON.stringify(newAuthState));
  },
  { deep: true }
);

export default store;
