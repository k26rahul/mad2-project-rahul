<template>
  <div class="container mt-4">
    <h1 class="text-primary fw-bold mb-4">User Management</h1>

    <!-- Loading state -->
    <div v-if="loading" class="text-center p-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- No users message -->
    <div v-else-if="users.length === 0" class="text-center p-5">
      <h3 class="text-muted">No users found</h3>
    </div>

    <!-- Users table -->
    <div v-else class="card border-0 shadow-lg rounded-4">
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-striped table-hover align-middle mb-0">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Date of Birth</th>
                <th>Qualification</th>
                <th>Role</th>
                <th>Total Attempts</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>{{ user.name }}</td>
                <td>{{ user.email }}</td>
                <td>{{ formatDate(user.dob) }}</td>
                <td>{{ formatQualification(user.qualification) }}</td>
                <td>
                  <span class="badge" :class="user.role === 'admin' ? 'bg-danger' : 'bg-primary'">
                    {{ user.role }}
                  </span>
                </td>
                <td>{{ user.total_attempts }}</td>
                <td>
                  <span class="badge" :class="user.active ? 'bg-success' : 'bg-warning'">
                    {{ user.active ? 'Active' : 'Blocked' }}
                  </span>
                </td>
                <td>
                  <button
                    v-if="user.role !== 'admin'"
                    class="btn btn-sm"
                    :class="user.active ? 'btn-warning' : 'btn-success'"
                    @click="toggleUserBlock(user)"
                  >
                    <i class="bi me-1" :class="user.active ? 'bi-lock' : 'bi-unlock'"></i>
                    {{ user.active ? 'Block' : 'Unblock' }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { get, put } from '@/utils/fetchHelper';

export default {
  data() {
    return {
      loading: true,
      users: [],
    };
  },

  methods: {
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      return new Date(dateString).toLocaleDateString();
    },

    formatQualification(qualification) {
      return qualification || 'N/A';
    },

    async toggleUserBlock(user) {
      try {
        const endpoint = user.active ? 'block' : 'unblock';
        const response = await put(`/api/admin/users/${user.id}/${endpoint}`);

        if (response.success) {
          // Update the user in the list
          const index = this.users.findIndex(u => u.id === user.id);
          this.users[index] = response.user;
        }
      } catch (error) {
        console.error('Failed to toggle user block status:', error);
        alert('Failed to update user status. Please try again.');
      }
    },

    async fetchUsers() {
      try {
        const response = await get('/api/admin/users');
        if (response.success) {
          this.users = response.users;
        }
      } catch (error) {
        console.error('Failed to fetch users:', error);
        alert('Failed to load users. Please try again.');
      } finally {
        this.loading = false;
      }
    },
  },

  mounted() {
    this.fetchUsers();
  },
};
</script>
