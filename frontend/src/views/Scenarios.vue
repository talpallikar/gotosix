<template>
  <div class="scenarios">
    <div class="header">
      <h1>Mulligan Scenarios</h1>
      <router-link v-if="authStore.isAuthenticated" to="/scenarios/new" class="btn btn-primary">
        Create Scenario
      </router-link>
    </div>

    <div v-if="loading" class="loading">Loading scenarios...</div>

    <div v-else-if="scenarioStore.scenarios.length === 0" class="empty">
      <p>No scenarios yet. Be the first to create one!</p>
    </div>

    <div v-else class="scenario-grid">
      <div v-for="scenario in scenarioStore.scenarios" :key="scenario._id" class="scenario-card">
        <h3>{{ scenario.num_cards }} Card Hand</h3>
        <div class="scenario-info">
          <p><strong>Position:</strong> {{ scenario.on_play ? 'On the Play' : 'On the Draw' }}</p>
          <p><strong>Opponent:</strong> {{ scenario.opponent_archetype }}</p>
          <p><strong>Game:</strong> {{ scenario.game_number }}</p>
        </div>
        <div class="votes">
          <span class="keep-votes">Keep: {{ scenario.keep_votes }}</span>
          <span class="mulligan-votes">Mulligan: {{ scenario.mulligan_votes }}</span>
        </div>
        <router-link :to="`/scenarios/${scenario._id}`" class="btn">View Details</router-link>
      </div>
    </div>

    <div v-if="scenarioStore.total > scenarioStore.perPage" class="pagination">
      <button
        @click="loadPage(scenarioStore.page - 1)"
        :disabled="scenarioStore.page === 1"
        class="btn"
      >
        Previous
      </button>
      <span>Page {{ scenarioStore.page }} of {{ Math.ceil(scenarioStore.total / scenarioStore.perPage) }}</span>
      <button
        @click="loadPage(scenarioStore.page + 1)"
        :disabled="scenarioStore.page * scenarioStore.perPage >= scenarioStore.total"
        class="btn"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useScenarioStore, useAuthStore } from '../store'

const scenarioStore = useScenarioStore()
const authStore = useAuthStore()
const loading = ref(true)

const loadPage = async (page) => {
  loading.value = true
  await scenarioStore.fetchScenarios(page)
  loading.value = false
}

onMounted(async () => {
  await loadPage(1)
})
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

h1 {
  color: #2c3e50;
}

.scenario-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.scenario-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.scenario-card h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.scenario-info {
  margin-bottom: 1rem;
}

.scenario-info p {
  margin: 0.5rem 0;
  color: #7f8c8d;
}

.votes {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 0.5rem 0;
  border-top: 1px solid #ecf0f1;
  border-bottom: 1px solid #ecf0f1;
}

.keep-votes {
  color: #27ae60;
  font-weight: bold;
}

.mulligan-votes {
  color: #e74c3c;
  font-weight: bold;
}

.btn {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #3498db;
  color: white;
  text-decoration: none;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn:hover:not(:disabled) {
  background: #2980b9;
}

.btn:disabled {
  background: #95a5a6;
  cursor: not-allowed;
}

.btn-primary {
  background: #2ecc71;
}

.btn-primary:hover {
  background: #27ae60;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.loading, .empty {
  text-align: center;
  padding: 3rem;
  color: #7f8c8d;
}
</style>
