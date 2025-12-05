<template>
  <div class="decklist-detail">
    <div v-if="loading" class="loading">Loading decklist...</div>

    <div v-else-if="decklistStore.currentDecklist" class="content">
      <div class="header">
        <div>
          <h1>{{ decklistStore.currentDecklist.name }}</h1>
          <p class="format">{{ decklistStore.currentDecklist.format }}</p>
          <p v-if="decklistStore.currentDecklist.archetype" class="archetype">
            {{ decklistStore.currentDecklist.archetype }}
          </p>
        </div>
        <div class="header-actions">
          <router-link
            v-if="authStore.isAuthenticated"
            :to="`/scenarios/new?decklist=${route.params.id}`"
            class="btn btn-primary"
          >
            Create Scenario
          </router-link>
          <router-link to="/decklists" class="btn">Back to Decklists</router-link>
        </div>
      </div>

      <div class="cards-container">
        <h2>Cards ({{ getTotalCards() }})</h2>
        <div class="card-list">
          <div v-for="card in decklistStore.currentDecklist.cards" :key="card.name" class="card-item">
            <span class="quantity">{{ card.quantity }}</span>
            <span class="name">{{ card.name }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useDecklistStore, useAuthStore } from '../store'

const route = useRoute()
const decklistStore = useDecklistStore()
const authStore = useAuthStore()

const loading = ref(true)

const getTotalCards = () => {
  return decklistStore.currentDecklist.cards.reduce((sum, card) => sum + card.quantity, 0)
}

onMounted(async () => {
  await decklistStore.fetchDecklist(route.params.id)
  loading.value = false
})
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #ecf0f1;
}

h1 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.format {
  color: #7f8c8d;
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
}

.archetype {
  color: #3498db;
  font-weight: 500;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.cards-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.card-list {
  display: grid;
  gap: 0.5rem;
}

.card-item {
  display: flex;
  gap: 1rem;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.quantity {
  font-weight: bold;
  color: #3498db;
  min-width: 2rem;
}

.name {
  color: #2c3e50;
}

.btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
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

.loading {
  text-align: center;
  padding: 3rem;
  color: #7f8c8d;
}
</style>
