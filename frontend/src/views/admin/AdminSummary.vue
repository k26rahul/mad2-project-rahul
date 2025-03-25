<template>
  <div class="container mt-4">
    <h1 class="text-primary fw-bold mb-4">Platform Statistics</h1>

    <!-- Loading state -->
    <div v-if="loading" class="text-center p-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else class="row g-4 mb-4">
      <!-- Platform Stats -->
      <div class="col-md-6 col-lg-3">
        <div class="card border-0 shadow-lg rounded-4 h-100">
          <div class="card-body text-center">
            <i class="bi bi-book fs-1 text-primary mb-2"></i>
            <h5 class="fw-bold">Total Subjects</h5>
            <h2 class="mb-0">{{ statistics.counts.subjects }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-6 col-lg-3">
        <div class="card border-0 shadow-lg rounded-4 h-100">
          <div class="card-body text-center">
            <i class="bi bi-journals fs-1 text-success mb-2"></i>
            <h5 class="fw-bold">Total Chapters</h5>
            <h2 class="mb-0">{{ statistics.counts.chapters }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-6 col-lg-3">
        <div class="card border-0 shadow-lg rounded-4 h-100">
          <div class="card-body text-center">
            <i class="bi bi-clipboard-check fs-1 text-warning mb-2"></i>
            <h5 class="fw-bold">Total Quizzes</h5>
            <h2 class="mb-0">{{ statistics.counts.quizzes }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-6 col-lg-3">
        <div class="card border-0 shadow-lg rounded-4 h-100">
          <div class="card-body text-center">
            <i class="bi bi-question-circle fs-1 text-info mb-2"></i>
            <h5 class="fw-bold">Total Questions</h5>
            <h2 class="mb-0">{{ statistics.counts.questions }}</h2>
          </div>
        </div>
      </div>

      <!-- Subject Stats -->
      <div class="col-md-6">
        <div class="card border-0 shadow-lg rounded-4">
          <div class="card-header bg-primary bg-opacity-10 border-0 rounded-top-4">
            <h4 class="fw-bold mb-0">Subject-wise Top Scores</h4>
          </div>
          <div class="card-body">
            <Bar :data="topScoresChart.data" :options="topScoresChart.options" />
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card border-0 shadow-lg rounded-4">
          <div class="card-header bg-primary bg-opacity-10 border-0 rounded-top-4">
            <h4 class="fw-bold mb-0">Subject-wise Attempts</h4>
          </div>
          <div class="card-body">
            <Radar :data="attemptsChart.data" :options="attemptsChart.options" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Bar, Radar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  RadialLinearScale,
  ArcElement,
  PointElement,
  LineElement,
} from 'chart.js';
import { get } from '@/utils/fetchHelper';

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  RadialLinearScale,
  ArcElement,
  PointElement,
  LineElement
);

export default {
  components: {
    Bar,
    Radar,
  },

  data() {
    return {
      loading: true,
      statistics: {
        counts: {
          subjects: 0,
          chapters: 0,
          quizzes: 0,
          questions: 0,
          attempts: 0,
        },
        subject_statistics: [],
      },
    };
  },

  computed: {
    topScoresChart() {
      const data = {
        labels: this.statistics.subject_statistics.map(s => s.name),
        datasets: [
          {
            label: 'Top Score (%)',
            data: this.statistics.subject_statistics.map(s => s.top_percentage || 0), // Add fallback to 0
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
          plugins: {
            legend: {
              display: false,
            },
            tooltip: {
              callbacks: {
                label: function (context) {
                  const value = context.parsed.y || 0;
                  return `Top Score: ${value.toFixed(1)}%`;
                },
              },
            },
          },
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
              ticks: {
                callback: value => `${value}%`, // Add % to y-axis labels
              },
            },
          },
        },
      };
    },

    attemptsChart() {
      const data = {
        labels: this.statistics.subject_statistics.map(s => s.name),
        datasets: [
          {
            label: 'Number of Attempts',
            data: this.statistics.subject_statistics.map(s => s.attempts),
            backgroundColor: 'rgba(13, 110, 253, 0.2)',
            borderColor: 'rgb(13, 110, 253)',
            borderWidth: 2,
            pointBackgroundColor: 'rgb(13, 110, 253)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(13, 110, 253)',
          },
        ],
      };
      return {
        data,
        options: {
          responsive: true,
          scales: {
            r: {
              beginAtZero: true,
              ticks: {
                stepSize: 1,
              },
            },
          },
          plugins: {
            legend: {
              display: true,
            },
          },
        },
      };
    },
  },

  async mounted() {
    try {
      const response = await get('/api/admin/statistics');
      this.statistics = response;
    } catch (error) {
      console.error('Failed to fetch statistics:', error);
    } finally {
      this.loading = false;
    }
  },
};
</script>
