<template>
  <div class="container mt-4">
    <!-- Quiz Details Card -->
    <div class="card border-0 shadow-lg rounded-4 mb-4">
      <div class="card-header bg-primary bg-opacity-10 border-0 rounded-top-4">
        <div class="d-flex justify-content-between align-items-center">
          <h3 class="fw-bold mb-0">{{ quiz.title }}</h3>
          <div v-if="started && quiz.duration" class="quiz-timer h4 mb-0 text-danger">
            <i class="bi bi-clock me-1"></i>
            {{ formatTime(timeLeft) }}
          </div>
        </div>
        <p class="text-muted mb-2">{{ quiz.description }}</p>
        <div class="d-flex gap-3">
          <small class="text-secondary">
            <i class="bi bi-journal me-1"></i>
            {{ quiz.chapter_name }} ({{ quiz.subject_name }})
          </small>
          <small class="text-secondary">
            <i class="bi bi-clock me-1"></i>
            {{ quiz.duration ? `${quiz.duration} minutes` : 'No time limit' }}
          </small>
        </div>
      </div>
    </div>

    <!-- Quiz Instructions & Start Button -->
    <div v-if="!started && !attempt" class="card border-0 shadow-lg rounded-4 mb-4">
      <div class="card-body">
        <h4 class="mb-3">Quiz Instructions</h4>
        <ul class="mb-4">
          <li>Each question carries 1 mark</li>
          <li v-if="quiz.duration">
            Quiz duration: {{ quiz.duration }} minutes <br />Quiz will be auto-submitted when time
            is over
          </li>
          <li v-else>This quiz has no time limit</li>
          <li>You can submit partial answers</li>
          <li>You cannot change your answers after submission</li>
        </ul>
        <div class="text-center">
          <p class="lead mb-4">Good luck! 🍀</p>
          <button @click="startQuiz" class="btn btn-primary btn-lg">
            <i class="bi bi-play-fill me-1"></i>
            Start Quiz
          </button>
        </div>
      </div>
    </div>

    <!-- Quiz Results -->
    <div v-if="attempt" class="card border-0 shadow-lg rounded-4 mb-4">
      <div class="card-body">
        <h4 class="text-center mb-4">Quiz Results</h4>
        <div class="row text-center">
          <div class="col-md-3">
            <div class="h3 mb-0">{{ attempt.correct_questions }}</div>
            <small class="text-success">Correct</small>
          </div>
          <div class="col-md-3">
            <div class="h3 mb-0">{{ attempt.incorrect_questions }}</div>
            <small class="text-danger">Incorrect</small>
          </div>
          <div class="col-md-3">
            <div class="h3 mb-0">{{ attempt.total_questions }}</div>
            <small class="text-muted">Total</small>
          </div>
          <div class="col-md-3">
            <div class="h3 mb-0" :class="getScoreClass(attempt.percentage)">
              {{ attempt.percentage.toFixed(1) }}%
            </div>
            <small class="text-muted">Score</small>
          </div>
        </div>
      </div>
    </div>

    <!-- Quiz Questions Section -->
    <div v-if="started" class="mb-4">
      <div
        v-for="question in questions"
        :key="question.id"
        class="card border-0 shadow-lg rounded-4 mb-4"
      >
        <div class="card-body">
          <h5 class="card-title mb-4">{{ question.statement }}</h5>

          <!-- Not Attempted Message (Only shown in results) -->
          <div v-if="attempt && !answerFeedback[question.id]" class="alert alert-warning mb-4">
            <i class="bi bi-dash-circle me-1"></i>
            Question not attempted
          </div>

          <div class="d-flex flex-column gap-3">
            <template v-if="!attempt">
              <!-- Radio inputs for attempting quiz -->
              <div v-for="(option, index) in getOptions(question)" :key="index" class="form-check">
                <input
                  :id="`q${question.id}o${index + 1}`"
                  class="form-check-input"
                  type="radio"
                  :name="`question${question.id}`"
                  :value="index + 1"
                  v-model="answers[question.id]"
                />
                <label class="form-check-label" :for="`q${question.id}o${index + 1}`">
                  {{ option }}
                </label>
              </div>
            </template>
            <template v-else>
              <!-- Results view with colored backgrounds and icons -->
              <div
                v-for="(option, index) in getOptions(question)"
                :key="index"
                class="p-2 rounded"
                :class="{
                  'bg-success bg-opacity-10': question.correct_option === index + 1,
                  'bg-danger bg-opacity-10':
                    answerFeedback[question.id]?.submitted === index + 1 &&
                    !answerFeedback[question.id]?.correct,
                }"
              >
                {{ option }}
                <i
                  v-if="question.correct_option === index + 1"
                  class="bi bi-check-circle-fill text-success ms-2"
                ></i>
                <i
                  v-else-if="answerFeedback[question.id]?.submitted === index + 1"
                  class="bi bi-x-circle-fill text-danger ms-2"
                ></i>
              </div>
            </template>
          </div>
        </div>
      </div>

      <!-- Submit Button (Only shown during attempt) -->
      <div v-if="!attempt" class="d-flex justify-content-center">
        <button @click="submitQuiz" class="btn btn-primary btn-lg">
          <i class="bi bi-check-lg me-1"></i>
          Submit Quiz
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { quizStore, questionStore, quizAttemptStore } from '@/store';
import confetti from 'canvas-confetti';

export default {
  data() {
    return {
      quiz: quizStore.quizzes.get(parseInt(this.$route.params.quiz_id)),
      started: false,
      timeLeft: 0,
      timer: null,
      answers: {},
      attempt: null,
      answerFeedback: {},
    };
  },

  computed: {
    questions() {
      return this.quiz.questions.map(id => questionStore.questions.get(id));
    },
  },

  methods: {
    getOptions(question) {
      return [question.option_a, question.option_b, question.option_c, question.option_d];
    },

    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = seconds % 60;
      return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    },

    startQuiz() {
      this.started = true;
      if (this.quiz.duration) {
        this.timeLeft = this.quiz.duration * 60;
        this.startTimer();
      }
    },

    startTimer() {
      this.timer = setInterval(() => {
        if (this.timeLeft > 0) {
          this.timeLeft--;
        } else {
          this.submitQuiz(true);
        }
      }, 1000);
    },

    celebrateSuccess() {
      // An initial center burst
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 },
      });

      // Two side cannon effects
      setTimeout(() => {
        confetti({
          particleCount: 50,
          angle: 60,
          spread: 55,
          origin: { x: 0 },
        });
        confetti({
          particleCount: 50,
          angle: 120,
          spread: 55,
          origin: { x: 1 },
        });
      }, 250);

      // A 360-degree spread with colorful particles
      setTimeout(() => {
        const defaults = {
          spread: 360,
          ticks: 50,
          gravity: 0,
          decay: 0.94,
          startVelocity: 30,
          colors: ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#00ffff'],
        };

        confetti({
          ...defaults,
          particleCount: 50,
          scalar: 2,
        });

        confetti({
          ...defaults,
          particleCount: 30,
          scalar: 3,
        });
      }, 500);
    },

    async submitQuiz(isAutoSubmit = false) {
      if (isAutoSubmit === true && this.quiz.duration) {
        alert('Time is up! Your quiz has been automatically submitted.');
      }

      if (Object.keys(this.answers).length === 0) {
        alert('Please answer at least one question before submitting.');
        return;
      }

      clearInterval(this.timer);

      const { attempt, answerFeedback } = await quizAttemptStore.create(this.quiz.id, this.answers);
      this.attempt = attempt;
      this.answerFeedback = answerFeedback;

      // Scroll to top
      window.scrollTo({ top: 0, behavior: 'smooth' });

      if (attempt.percentage >= 80) {
        setTimeout(() => this.celebrateSuccess(), 1000);
      }
    },

    getScoreClass(percentage) {
      if (percentage >= 80) return 'text-success';
      if (percentage >= 60) return 'text-primary';
      if (percentage >= 40) return 'text-warning';
      return 'text-danger';
    },
  },

  beforeUnmount() {
    if (this.timer) {
      clearInterval(this.timer);
    }
  },
};
</script>
