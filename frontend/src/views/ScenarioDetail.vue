<template>
  <div class="scenario-detail">
    <div v-if="loading" class="loading">Loading scenario...</div>

    <div v-else-if="scenarioStore.currentScenario" class="content">
      <div class="header">
        <h1>Mulligan Decision</h1>
        <router-link to="/scenarios" class="btn">Back to Scenarios</router-link>
      </div>

      <div class="scenario-container">
        <div class="scenario-info">
          <h2>Scenario Details</h2>
          <div class="info-grid">
            <div class="info-item">
              <strong>Cards in Hand:</strong>
              <span>{{ scenarioStore.currentScenario.num_cards }}</span>
            </div>
            <div class="info-item">
              <strong>Position:</strong>
              <span>{{ scenarioStore.currentScenario.on_play ? 'On the Play' : 'On the Draw' }}</span>
            </div>
            <div class="info-item">
              <strong>Opponent Archetype:</strong>
              <span>{{ scenarioStore.currentScenario.opponent_archetype }}</span>
            </div>
            <div class="info-item">
              <strong>Game Number:</strong>
              <span>{{ scenarioStore.currentScenario.game_number }}</span>
            </div>
          </div>

          <div class="hand">
            <h3 v-if="scenarioStore.currentScenario.mulligan_count > 0">
              London Mulligan: Select {{ scenarioStore.currentScenario.mulligan_count }} card{{ scenarioStore.currentScenario.mulligan_count > 1 ? 's' : '' }} to put on bottom
            </h3>
            <h3 v-else>Your Opening Hand:</h3>

            <div class="mulligan-instructions" v-if="scenarioStore.currentScenario.mulligan_count > 0 && !mulliganComplete">
              <p>
                <strong>How London Mulligan Works:</strong><br>
                You drew 7 cards and decided to mulligan. Now select {{ scenarioStore.currentScenario.mulligan_count }} card{{ scenarioStore.currentScenario.mulligan_count > 1 ? 's' : '' }} to put on the bottom of your library.
                After that, you'll decide whether to keep the remaining {{ scenarioStore.currentScenario.num_cards }} or mulligan again.
              </p>
            </div>

            <div class="card-grid" :class="{ 'selection-mode': scenarioStore.currentScenario.mulligan_count > 0 && !mulliganComplete }">
              <div
                v-for="(card, index) in displayedHand"
                :key="index"
                class="card-wrapper"
                :class="{
                  'selected': selectedCards.includes(index),
                  'selectable': scenarioStore.currentScenario.mulligan_count > 0 && !mulliganComplete
                }"
                @click="toggleCardSelection(index)"
              >
                <MtgCard
                  :card-name="card"
                  size="normal"
                />
                <div v-if="selectedCards.includes(index)" class="selection-badge">
                  Bottoming
                </div>
              </div>
            </div>

            <div v-if="scenarioStore.currentScenario.mulligan_count > 0 && !mulliganComplete" class="mulligan-actions">
              <button
                @click="confirmSelection"
                class="btn btn-confirm"
                :disabled="selectedCards.length !== scenarioStore.currentScenario.mulligan_count"
              >
                Confirm Selection ({{ selectedCards.length }}/{{ scenarioStore.currentScenario.mulligan_count }})
              </button>
              <button @click="clearSelection" class="btn btn-secondary">
                Clear Selection
              </button>
            </div>
          </div>

          <div v-if="scenarioStore.currentScenario.decklist" class="decklist-info">
            <h3>Decklist</h3>
            <router-link :to="`/decklists/${scenarioStore.currentScenario.decklist._id}`">
              {{ scenarioStore.currentScenario.decklist.name }}
              <span v-if="scenarioStore.currentScenario.decklist.archetype">
                ({{ scenarioStore.currentScenario.decklist.archetype }})
              </span>
            </router-link>
          </div>
        </div>

        <div class="voting-section">
          <h2>What's Your Decision?</h2>

          <div class="vote-stats">
            <div class="stat keep">
              <div class="count">{{ scenarioStore.currentScenario.keep_votes }}</div>
              <div class="label">Keep</div>
            </div>
            <div class="stat mulligan">
              <div class="count">{{ scenarioStore.currentScenario.mulligan_votes }}</div>
              <div class="label">Mulligan</div>
            </div>
          </div>

          <div v-if="authStore.isAuthenticated" class="vote-buttons">
            <p v-if="userVote" class="current-vote">
              You voted: <strong>{{ userVote.decision }}</strong>
            </p>
            <button @click="vote('keep')" class="btn btn-keep" :disabled="voting">
              {{ userVote?.decision === 'keep' ? 'Voted Keep' : 'Vote Keep' }}
            </button>
            <button @click="vote('mulligan')" class="btn btn-mulligan" :disabled="voting">
              {{ userVote?.decision === 'mulligan' ? 'Voted Mulligan' : 'Vote Mulligan' }}
            </button>
          </div>

          <div v-else class="login-prompt">
            <p>Please <router-link to="/login">login</router-link> to vote</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useScenarioStore, useAuthStore } from '../store'
import MtgCard from '../components/MtgCard.vue'

const route = useRoute()
const scenarioStore = useScenarioStore()
const authStore = useAuthStore()

const loading = ref(true)
const voting = ref(false)
const userVote = ref(null)
const selectedCards = ref([])
const mulliganComplete = ref(false)
const displayedHand = ref([])

const loadScenario = async () => {
  loading.value = true
  await scenarioStore.fetchScenario(route.params.id)
  if (authStore.isAuthenticated) {
    userVote.value = await scenarioStore.getUserVote(route.params.id)
  }

  // Initialize displayed hand
  displayedHand.value = [...scenarioStore.currentScenario.hand]
  mulliganComplete.value = scenarioStore.currentScenario.mulligan_count === 0

  loading.value = false
}

const toggleCardSelection = (index) => {
  if (mulliganComplete.value || scenarioStore.currentScenario.mulligan_count === 0) {
    return // Can't select cards if mulligan is complete or no mulligan needed
  }

  const cardIndex = selectedCards.value.indexOf(index)

  if (cardIndex > -1) {
    // Deselect card
    selectedCards.value.splice(cardIndex, 1)
  } else {
    // Select card (only if we haven't reached the limit)
    if (selectedCards.value.length < scenarioStore.currentScenario.mulligan_count) {
      selectedCards.value.push(index)
    }
  }
}

const confirmSelection = () => {
  if (selectedCards.value.length !== scenarioStore.currentScenario.mulligan_count) {
    return
  }

  // Remove selected cards from displayed hand (they're being bottomed)
  displayedHand.value = scenarioStore.currentScenario.hand.filter((_, index) => !selectedCards.value.includes(index))
  mulliganComplete.value = true
}

const clearSelection = () => {
  selectedCards.value = []
}

const vote = async (decision) => {
  voting.value = true
  try {
    await scenarioStore.vote(route.params.id, decision)
    userVote.value = await scenarioStore.getUserVote(route.params.id)
  } catch (err) {
    console.error('Vote failed:', err)
  }
  voting.value = false
}

onMounted(loadScenario)
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.scenario-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.scenario-info, .voting-section {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

h3 {
  color: #2c3e50;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
}

.info-grid {
  display: grid;
  gap: 1rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.hand {
  margin-top: 1.5rem;
}

.mulligan-instructions {
  background: #e3f2fd;
  border-left: 4px solid #2196f3;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 4px;
}

.mulligan-instructions p {
  margin: 0;
  color: #1976d2;
  line-height: 1.6;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.card-grid.selection-mode {
  gap: 1.5rem;
}

.card-wrapper {
  position: relative;
  cursor: default;
}

.card-wrapper.selectable {
  cursor: pointer;
  transition: transform 0.2s;
}

.card-wrapper.selectable:hover {
  transform: translateY(-8px);
}

.card-wrapper.selected {
  opacity: 0.6;
}

.selection-badge {
  position: absolute;
  top: -10px;
  right: -10px;
  background: #e74c3c;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.mulligan-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  justify-content: center;
}

.btn-confirm {
  background: #2ecc71;
}

.btn-confirm:hover:not(:disabled) {
  background: #27ae60;
}

.btn-confirm:disabled {
  background: #95a5a6;
  cursor: not-allowed;
}

.btn-secondary {
  background: #95a5a6;
}

.btn-secondary:hover {
  background: #7f8c8d;
}

.decklist-info a {
  color: #3498db;
  text-decoration: none;
}

.vote-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat {
  text-align: center;
  padding: 1.5rem;
  border-radius: 8px;
}

.stat.keep {
  background: #d5f4e6;
}

.stat.mulligan {
  background: #fadbd8;
}

.count {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.stat.keep .count {
  color: #27ae60;
}

.stat.mulligan .count {
  color: #e74c3c;
}

.label {
  font-size: 1.1rem;
  color: #7f8c8d;
}

.vote-buttons {
  display: grid;
  gap: 1rem;
}

.current-vote {
  text-align: center;
  margin-bottom: 1rem;
  color: #7f8c8d;
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
  font-size: 1rem;
  transition: background 0.2s;
}

.btn:hover:not(:disabled) {
  background: #2980b9;
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-keep {
  background: #27ae60;
}

.btn-keep:hover:not(:disabled) {
  background: #229954;
}

.btn-mulligan {
  background: #e74c3c;
}

.btn-mulligan:hover:not(:disabled) {
  background: #c0392b;
}

.login-prompt {
  text-align: center;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.login-prompt a {
  color: #3498db;
  text-decoration: none;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #7f8c8d;
}

@media (max-width: 768px) {
  .scenario-container {
    grid-template-columns: 1fr;
  }
}
</style>
