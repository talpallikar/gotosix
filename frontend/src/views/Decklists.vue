<template>
  <div class="decklists">
    <div class="header">
      <h1>Decklists</h1>
      <router-link v-if="authStore.isAuthenticated" to="/decklists/new" class="btn btn-primary">
        Upload Decklist
      </router-link>
    </div>

    <div class="tabs">
      <button @click="activeTab = 'all'" :class="{ active: activeTab === 'all' }" class="tab">
        All Decklists
      </button>
      <button
        v-if="authStore.isAuthenticated"
        @click="loadMyDecklists"
        :class="{ active: activeTab === 'mine' }"
        class="tab"
      >
        My Decklists
      </button>
    </div>

    <div v-if="loading" class="loading">Loading decklists...</div>

    <div v-else-if="currentDecklists.length === 0" class="empty">
      <p>No decklists yet. Be the first to upload one!</p>
    </div>

    <div v-else class="decklist-grid">
      <div v-for="decklist in currentDecklists" :key="decklist._id" class="decklist-card">
        <h3>{{ decklist.name }}</h3>
        <div class="decklist-info">
          <p><strong>Format:</strong> {{ decklist.format }}</p>
          <p v-if="decklist.archetype"><strong>Archetype:</strong> {{ decklist.archetype }}</p>
          <p><strong>Cards:</strong> {{ getTotalCards(decklist.cards) }}</p>
        </div>
        <router-link :to="`/decklists/${decklist._id}`" class="btn">View Decklist</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useDecklistStore, useAuthStore } from '../store'

const decklistStore = useDecklistStore()
const authStore = useAuthStore()

const loading = ref(true)
const activeTab = ref('all')

const currentDecklists = computed(() => {
  return activeTab.value === 'all' ? decklistStore.decklists : decklistStore.myDecklists
})

const getTotalCards = (cards) => {
  return cards.reduce((sum, card) => sum + card.quantity, 0)
}

const loadMyDecklists = async () => {
  activeTab.value = 'mine'
  loading.value = true
  await decklistStore.fetchMyDecklists()
  loading.value = false
}

onMounted(async () => {
  await decklistStore.fetchDecklists()
  loading.value = false
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

.tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 2px solid #ecf0f1;
}

.tab {
  padding: 0.75rem 1.5rem;
  background: none;
  border: none;
  color: #7f8c8d;
  cursor: pointer;
  font-size: 1rem;
  transition: color 0.2s;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
}

.tab:hover {
  color: #2c3e50;
}

.tab.active {
  color: #3498db;
  border-bottom-color: #3498db;
}

.decklist-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.decklist-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.decklist-card h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.decklist-info {
  margin-bottom: 1rem;
}

.decklist-info p {
  margin: 0.5rem 0;
  color: #7f8c8d;
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

.btn:hover {
  background: #2980b9;
}

.btn-primary {
  background: #2ecc71;
}

.btn-primary:hover {
  background: #27ae60;
}

.loading, .empty {
  text-align: center;
  padding: 3rem;
  color: #7f8c8d;
}
</style>
