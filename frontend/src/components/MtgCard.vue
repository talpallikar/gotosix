<template>
  <div class="mtg-card" :class="{ loading: isLoading, error: hasError }">
    <div v-if="isLoading" class="card-loading">
      <div class="spinner"></div>
      <p>{{ cardName }}</p>
    </div>

    <div v-else-if="hasError" class="card-error">
      <div class="error-icon">?</div>
      <p>{{ cardName }}</p>
    </div>

    <div v-else class="card-image-container">
      <img
        :src="imageUrl"
        :alt="cardName"
        class="card-image"
        @error="handleImageError"
      />
      <div v-if="showName" class="card-name-overlay">
        {{ cardName }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import scryfallApi from '../api/scryfall'

const props = defineProps({
  cardName: {
    type: String,
    required: true
  },
  size: {
    type: String,
    default: 'normal',
    validator: (value) => ['small', 'normal', 'large', 'png', 'art_crop', 'border_crop'].includes(value)
  },
  showName: {
    type: Boolean,
    default: false
  }
})

const imageUrl = ref(null)
const isLoading = ref(true)
const hasError = ref(false)

const loadCardImage = async () => {
  isLoading.value = true
  hasError.value = false

  try {
    const card = await scryfallApi.getCardByName(props.cardName)
    if (card) {
      imageUrl.value = scryfallApi.getCardImageUrl(card, props.size)
      if (!imageUrl.value) {
        hasError.value = true
      }
    } else {
      hasError.value = true
    }
  } catch (error) {
    console.error('Error loading card:', props.cardName, error)
    hasError.value = true
  } finally {
    isLoading.value = false
  }
}

const handleImageError = () => {
  hasError.value = true
}

onMounted(() => {
  loadCardImage()
})

// Reload if card name changes
watch(() => props.cardName, () => {
  loadCardImage()
})
</script>

<style scoped>
.mtg-card {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  background: #1a1a1a;
  aspect-ratio: 5 / 7;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s, box-shadow 0.2s;
}

.mtg-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.card-loading,
.card-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  text-align: center;
  width: 100%;
  height: 100%;
}

.card-loading p,
.card-error p {
  color: #ecf0f1;
  font-size: 0.9rem;
  margin-top: 0.5rem;
  word-wrap: break-word;
  max-width: 100%;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #34495e;
  border-top-color: #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #e74c3c;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
}

.card-image-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.card-name-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 0.5rem;
  font-size: 0.85rem;
  text-align: center;
  backdrop-filter: blur(4px);
}
</style>
