<template>
  <div class="container mt-4">
    <h1 class="text-primary fw-bold mb-4">Your Learning Summary</h1>

    <!-- No attempts message -->
    <div v-if="!lastAttempt" class="text-center p-5">
      <h3 class="text-muted">No quiz attempts yet</h3>
      <p class="lead">Start attempting quizzes to see your analytics here!</p>
      <router-link to="/user/home" class="btn btn-primary btn-lg">
        <i class="bi bi-play-fill me-1"></i>
        Browse Quizzes
      </router-link>
    </div>

    <div v-else class="row g-4 mb-4">
      <!-- Quick Stats -->
      <div class="col-md-6 col-lg-3">
        <div class="card border-0 shadow-lg rounded-4 h-100">
          <div class="card-body text-center">
            <i class="bi bi-journals fs-1 text-primary mb-2"></i>
            <h5 class="fw-bold">Total Attempts</h5>
            <h2 class="mb-0">{{ totalAttempts }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-6 col-lg-3">
        <div class="card border-0 shadow-lg rounded-4 h-100">
          <div class="card-body text-center">
            <i class="bi bi-bullseye fs-1 text-success mb-2"></i>
            <h5 class="fw-bold">Overall Accuracy</h5>
            <h2 class="mb-0">{{ overallAccuracy.toFixed(1) }}%</h2>
          </div>
        </div>
      </div>

      <div class="col-md-6 col-lg-3">
        <div class="card border-0 shadow-lg rounded-4 h-100">
          <div class="card-body text-center">
            <i class="bi bi-trophy fs-1 text-warning mb-2"></i>
            <h5 class="fw-bold">Best Score</h5>
            <h2 class="mb-0">{{ bestScore.toFixed(1) }}%</h2>
          </div>
        </div>
      </div>

      <div class="col-md-6 col-lg-3">
        <div class="card border-0 shadow-lg rounded-4 h-100">
          <div class="card-body text-center">
            <i class="bi bi-calendar-check fs-1 text-info mb-2"></i>
            <h5 class="fw-bold">Active Months</h5>
            <h2 class="mb-0">{{ uniqueMonths }}</h2>
          </div>
        </div>
      </div>

      <!-- Last Attempt -->
      <div class="col-12">
        <div class="card border-0 shadow-lg rounded-4">
          <div class="card-header bg-primary bg-opacity-10 border-0 rounded-top-4">
            <h4 class="fw-bold mb-0">Last Attempt</h4>
          </div>
          <div class="card-body">
            <div class="row align-items-center">
              <div class="col-md-4">
                <h5 class="mb-1">{{ lastAttempt.quiz_title }}</h5>
                <small class="text-secondary">
                  <i class="bi bi-journal me-1"></i>
                  {{ lastAttempt.chapter_name }} ({{ lastAttempt.subject_name }})
                </small>
                <br />
                <small class="text-muted">
                  <i class="bi bi-clock-history me-1"></i>
                  {{ new Date(lastAttempt.attempted_at).toLocaleString() }}
                </small>
              </div>
              <div class="col-md-5">
                <div class="d-flex gap-4 justify-content-center">
                  <div class="text-center">
                    <div class="h4 mb-0">{{ lastAttempt.correct_questions }}</div>
                    <small class="text-success">Correct</small>
                  </div>
                  <div class="text-center">
                    <div class="h4 mb-0">{{ lastAttempt.incorrect_questions }}</div>
                    <small class="text-danger">Incorrect</small>
                  </div>
                  <div class="text-center">
                    <div class="h4 mb-0">{{ lastAttempt.total_questions }}</div>
                    <small class="text-muted">Total</small>
                  </div>
                </div>
              </div>
              <div class="col-md-3 text-end">
                <h3 class="mb-0" :class="getScoreClass(lastAttempt.percentage)">
                  {{ lastAttempt.percentage.toFixed(1) }}%
                </h3>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Section -->
      <h2 class="text-primary fw-bold mb-4">Learning Analytics</h2>

      <div class="row g-4">
        <!-- Subject-wise Stats -->
        <div class="col-md-6">
          <div class="card border-0 shadow-lg rounded-4">
            <div class="card-header bg-primary bg-opacity-10 border-0 rounded-top-4">
              <h4 class="fw-bold mb-0">Subject-wise Attempts</h4>
            </div>
            <div class="card-body" style="height: 300px">
              <Bar :data="subjectAttemptsChart.data" :options="subjectAttemptsChart.options" />
            </div>
          </div>
        </div>

        <div class="col-md-6">
          <div class="card border-0 shadow-lg rounded-4">
            <div class="card-header bg-primary bg-opacity-10 border-0 rounded-top-4">
              <h4 class="fw-bold mb-0">Subject-wise Accuracy</h4>
            </div>
            <div class="card-body" style="height: 300px">
              <Bar :data="subjectAccuracyChart.data" :options="subjectAccuracyChart.options" />
            </div>
          </div>
        </div>

        <!-- Monthly Activity -->
        <div class="col-md-6">
          <div class="card border-0 shadow-lg rounded-4">
            <div class="card-header bg-primary bg-opacity-10 border-0 rounded-top-4">
              <h4 class="fw-bold mb-0">Monthly Activity</h4>
            </div>
            <div class="card-body" style="height: 300px">
              <Pie :data="monthlyActivityChart.data" :options="monthlyActivityChart.options" />
            </div>
          </div>
        </div>

        <!-- Export Section -->
        <div class="col-12">
          <div class="card border-0 shadow-lg rounded-4">
            <div class="card-header bg-primary bg-opacity-10 border-0 rounded-top-4">
              <h4 class="fw-bold mb-0">Export Your Data</h4>
            </div>
            <div class="card-body text-center">
              <p class="lead mb-4">
                Download a detailed report of all your quiz attempts in CSV format.
                <br />
                <small class="text-muted">
                  Includes quiz details, scores, rankings, and attempt timestamps.
                </small>
              </p>
              <button class="btn btn-primary btn-lg" @click="exportData" :disabled="isExporting">
                <i class="bi bi-download me-2"></i>
                {{ isExporting ? 'Requesting Export...' : 'Export Quiz History' }}
              </button>
              <div v-if="exportMessage" class="alert alert-success mt-3">
                <i class="bi bi-envelope-check me-2"></i>
                {{ exportMessage }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Bar, Pie } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
} from 'chart.js';
import { quizAttemptStore, subjectStore } from '@/store';
import { post } from '@/utils/fetchHelper';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement);

export default {
  components: {
    Bar,
    Pie,
  },

  data() {
    return {
      isExporting: false,
      exportMessage: '',
    };
  },

  computed: {
    attempts() {
      return Array.from(quizAttemptStore.attempts.values());
    },

    totalAttempts() {
      return this.attempts.length;
    },

    lastAttempt() {
      if (!this.attempts.length) return null;
      return [...this.attempts].sort(
        (a, b) => new Date(b.attempted_at) - new Date(a.attempted_at)
      )[0];
    },

    overallAccuracy() {
      if (!this.attempts.length) return 0;
      return (
        this.attempts.reduce((sum, attempt) => sum + attempt.percentage, 0) / this.attempts.length
      );
    },

    bestScore() {
      if (!this.attempts.length) return 0;
      return Math.max(...this.attempts.map(a => a.percentage));
    },

    uniqueMonths() {
      if (!this.attempts.length) return 0;
      const months = new Set(
        this.attempts.map(a => new Date(a.attempted_at).toISOString().slice(0, 7))
      );
      return months.size;
    },

    subjectAttemptsChart() {
      const subjects = Array.from(subjectStore.subjects.values());
      const data = {
        labels: subjects.map(s => s.name),
        datasets: [
          {
            label: 'Number of Attempts',
            data: subjects.map(s => this.attempts.filter(a => a.subject_name === s.name).length),
            backgroundColor: 'rgba(13, 110, 253, 0.5)',
            borderColor: 'rgb(13, 110, 253)',
            borderWidth: 1,
          },
        ],
      };
      return {
        data,
        options: {
          responsive: true,
          maintainAspectRatio: true,
          aspectRatio: 1.5,
          plugins: {
            legend: {
              display: false,
            },
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1,
              },
            },
          },
        },
      };
    },

    subjectAccuracyChart() {
      const subjects = Array.from(subjectStore.subjects.values());
      const data = {
        labels: subjects.map(s => s.name),
        datasets: [
          {
            label: 'Average Accuracy',
            data: subjects.map(s => {
              const subjectAttempts = this.attempts.filter(a => a.subject_name === s.name);
              if (!subjectAttempts.length) return 0;
              return (
                subjectAttempts.reduce((sum, a) => sum + a.percentage, 0) / subjectAttempts.length
              );
            }),
            backgroundColor: 'rgba(25, 135, 84, 0.5)',
            borderColor: 'rgb(25, 135, 84)',
            borderWidth: 1,
          },
        ],
      };
      return {
        data,
        options: {
          responsive: true,
          maintainAspectRatio: true,
          aspectRatio: 1.5,
          plugins: {
            legend: {
              display: false,
            },
          },
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
            },
          },
        },
      };
    },

    monthlyActivityChart() {
      const monthCounts = {};
      this.attempts.forEach(attempt => {
        const month = new Date(attempt.attempted_at).toLocaleString('default', {
          month: 'long',
        });
        monthCounts[month] = (monthCounts[month] || 0) + 1;
      });

      const data = {
        labels: Object.keys(monthCounts),
        datasets: [
          {
            data: Object.values(monthCounts),
            backgroundColor: [
              'rgba(13, 110, 253, 0.5)',
              'rgba(25, 135, 84, 0.5)',
              'rgba(255, 193, 7, 0.5)',
              'rgba(220, 53, 69, 0.5)',
              'rgba(13, 202, 240, 0.5)',
            ],
            borderColor: [
              'rgb(13, 110, 253)',
              'rgb(25, 135, 84)',
              'rgb(255, 193, 7)',
              'rgb(220, 53, 69)',
              'rgb(13, 202, 240)',
            ],
            borderWidth: 1,
          },
        ],
      };

      return {
        data,
        options: {
          responsive: true,
          maintainAspectRatio: true,
          aspectRatio: 1.5,
          plugins: {
            legend: {
              position: 'right',
            },
          },
        },
      };
    },
  },

  methods: {
    getScoreClass(percentage) {
      if (percentage >= 80) return 'text-success';
      if (percentage >= 60) return 'text-primary';
      if (percentage >= 40) return 'text-warning';
      return 'text-danger';
    },

    async exportData() {
      this.isExporting = true;
      try {
        const response = await post('/api/user/export-attempts');
        if (response.success) {
          this.exportMessage = response.message;
        }
      } catch (error) {
        console.error('Export failed:', error);
        this.exportMessage = 'Failed to initiate export. Please try again.';
      } finally {
        this.isExporting = false;
      }
    },
  },
};
</script>
