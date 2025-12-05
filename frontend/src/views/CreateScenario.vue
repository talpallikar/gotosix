<template>
  <div class="create-scenario">
    <div class="header">
      <h1>Create Mulligan Scenario</h1>
      <router-link to="/scenarios" class="btn">Back</router-link>
    </div>

    <div class="form-container">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Select Decklist *</label>
          <select v-model="form.decklist_id" required @change="loadDecklist">
            <option value="">Choose a decklist</option>
            <option v-for="deck in decklists" :key="deck._id" :value="deck._id">
              {{ deck.name }} ({{ deck.format }})
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Number of Cards in Hand *</label>
          <select v-model.number="form.num_cards" required>
            <option :value="7">7 Cards (Opening hand)</option>
            <option :value="6">6 Cards (1 Mulligan)</option>
            <option :value="5">5 Cards (2 Mulligans)</option>
            <option :value="4">4 Cards (3 Mulligans)</option>
            <option :value="3">3 Cards (4 Mulligans)</option>
            <option :value="2">2 Cards (5 Mulligans)</option>
            <option :value="1">1 Card (6 Mulligans)</option>
          </select>
        </div>

        <div class="form-group">
          <label>Position *</label>
          <div class="radio-group">
            <label class="radio-label">
              <input v-model="form.on_play" type="radio" :value="true" />
              On the Play (going first)
            </label>
            <label class="radio-label">
              <input v-model="form.on_play" type="radio" :value="false" />
              On the Draw (going second)
            </label>
          </div>
        </div>

        <div class="form-group">
          <label>Opponent's Archetype *</label>
          <div v-if="!showCustomOpponentArchetype">
            <select v-model="form.opponent_archetype" required>
              <option value="">Select opponent's archetype</option>
              <option v-for="archetype in opponentArchetypes" :key="archetype" :value="archetype">
                {{ archetype }}
              </option>
            </select>
            <button
              type="button"
              @click="toggleCustomOpponentArchetype"
              class="btn-link custom-archetype-toggle"
              v-if="selectedDecklistFormat"
            >
              My archetype isn't present
            </button>
            <p class="help-text" v-if="selectedDecklistFormat">
              Showing {{ selectedDecklistFormat }} archetypes
            </p>
          </div>
          <div v-else>
            <input
              v-model="customOpponentArchetype"
              type="text"
              placeholder="Enter opponent's custom archetype"
              required
            />
            <button
              type="button"
              @click="toggleCustomOpponentArchetype"
              class="btn-link custom-archetype-toggle"
            >
              Choose from list instead
            </button>
            <p class="help-text">Enter a custom opponent archetype</p>
          </div>
        </div>

        <div class="form-group">
          <label>Game Number *</label>
          <select v-model.number="form.game_number" required>
            <option :value="1">Game 1 (Pre-sideboard)</option>
            <option :value="2">Game 2 (Post-sideboard)</option>
            <option :value="3">Game 3 (Post-sideboard)</option>
          </select>
        </div>

        <div v-if="error" class="error">{{ error }}</div>

        <button type="submit" class="btn btn-primary" :disabled="submitting">
          {{ submitting ? 'Creating...' : 'Create Scenario' }}
        </button>
      </form>

      <div v-if="preview" class="preview">
        <h3>Preview Hand:</h3>
        <div class="preview-cards">
          <MtgCard
            v-for="(card, index) in preview"
            :key="index"
            :card-name="card"
            size="normal"
          />
        </div>
        <p class="preview-note">Note: This is a preview. The actual hand will be randomly generated when you create the scenario.</p>
        <button type="button" @click="loadDecklist" class="btn btn-refresh">
          Shuffle New Hand
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useScenarioStore, useDecklistStore } from '../store'
import MtgCard from '../components/MtgCard.vue'
import { getArchetypesForFormat } from '../data/archetypes'

const router = useRouter()
const route = useRoute()
const scenarioStore = useScenarioStore()
const decklistStore = useDecklistStore()

const form = ref({
  decklist_id: route.query.decklist || '',
  num_cards: 7,
  on_play: true,
  opponent_archetype: '',
  game_number: 1
})

const decklists = ref([])
const preview = ref(null)
const error = ref('')
const submitting = ref(false)
const showCustomOpponentArchetype = ref(false)
const customOpponentArchetype = ref('')

// Get selected decklist format
const selectedDecklistFormat = computed(() => {
  if (!form.value.decklist_id) return null
  const decklist = decklists.value.find(d => d._id === form.value.decklist_id)
  return decklist?.format || null
})

// Get opponent archetypes based on decklist format
const opponentArchetypes = computed(() => {
  if (!selectedDecklistFormat.value) {
    return []
  }
  return getArchetypesForFormat(selectedDecklistFormat.value)
})

// Reset opponent archetype when decklist changes
watch(() => form.value.decklist_id, () => {
  form.value.opponent_archetype = ''
  showCustomOpponentArchetype.value = false
  customOpponentArchetype.value = ''
})

const toggleCustomOpponentArchetype = () => {
  showCustomOpponentArchetype.value = !showCustomOpponentArchetype.value
  if (showCustomOpponentArchetype.value) {
    // Switching to custom input
    customOpponentArchetype.value = form.value.opponent_archetype || ''
    form.value.opponent_archetype = ''
  } else {
    // Switching back to dropdown
    form.value.opponent_archetype = customOpponentArchetype.value || ''
    customOpponentArchetype.value = ''
  }
}

const loadDecklist = () => {
  if (form.value.decklist_id) {
    const decklist = decklists.value.find(d => d._id === form.value.decklist_id)
    if (decklist) {
      generatePreview(decklist)
    }
  }
}

const generatePreview = (decklist) => {
  const deck = []
  for (const card of decklist.cards) {
    for (let i = 0; i < card.quantity; i++) {
      deck.push(card.name)
    }
  }

  const numCards = Math.min(form.value.num_cards, deck.length)
  const shuffled = deck.sort(() => Math.random() - 0.5)
  preview.value = shuffled.slice(0, numCards)
}

const handleSubmit = async () => {
  submitting.value = true
  error.value = ''

  // Use custom opponent archetype if present
  const finalOpponentArchetype = showCustomOpponentArchetype.value
    ? customOpponentArchetype.value
    : form.value.opponent_archetype

  try {
    const scenario = await scenarioStore.createScenario({
      decklist_id: form.value.decklist_id,
      num_cards: form.value.num_cards,
      on_play: form.value.on_play,
      opponent_archetype: finalOpponentArchetype,
      game_number: form.value.game_number
    })

    router.push(`/scenarios/${scenario._id}`)
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to create scenario'
  }

  submitting.value = false
}

// Watch for changes in num_cards to regenerate preview
watch(() => form.value.num_cards, () => {
  if (form.value.decklist_id) {
    loadDecklist()
  }
})

onMounted(async () => {
  await decklistStore.fetchDecklists()
  decklists.value = decklistStore.decklists

  if (form.value.decklist_id) {
    loadDecklist()
  }
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

.form-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  max-width: 800px;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

input, select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:focus, select:focus {
  outline: none;
  border-color: #3498db;
}

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 4px;
  transition: background 0.2s;
}

.radio-label:hover {
  background: #e9ecef;
}

.radio-label input[type="radio"] {
  width: auto;
  margin: 0;
}

.error {
  color: #e74c3c;
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: #fadbd8;
  border-radius: 4px;
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
  background: #95a5a6;
  cursor: not-allowed;
}

.btn-primary {
  background: #2ecc71;
}

.btn-primary:hover:not(:disabled) {
  background: #27ae60;
}

.preview {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.preview h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.preview-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.btn-refresh {
  background: #9b59b6;
  margin-top: 1rem;
}

.btn-refresh:hover:not(:disabled) {
  background: #8e44ad;
}

.preview-note {
  font-size: 0.9rem;
  color: #7f8c8d;
  font-style: italic;
}

.custom-archetype-toggle {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.85rem;
}
</style>
