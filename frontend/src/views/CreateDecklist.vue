<template>
  <div class="create-decklist">
    <div class="header">
      <h1>Upload Decklist</h1>
      <router-link to="/decklists" class="btn">Back</router-link>
    </div>

    <div class="form-container">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Deck Name *</label>
          <input v-model="form.name" type="text" required placeholder="e.g., Mono Red Aggro" />
        </div>

        <div class="form-group">
          <label>Format *</label>
          <select v-model="form.format" required>
            <option value="">Select a format</option>
            <option value="Standard">Standard</option>
            <option value="Modern">Modern</option>
            <option value="Pioneer">Pioneer</option>
            <option value="Legacy">Legacy</option>
            <option value="Vintage">Vintage</option>
            <option value="Commander">Commander</option>
            <option value="Pauper">Pauper</option>
          </select>
        </div>

        <div class="form-group">
          <label>Archetype (optional)</label>
          <input v-model="form.archetype" type="text" placeholder="e.g., Aggro, Control, Midrange" />
        </div>

        <div class="form-group">
          <label>Decklist *</label>

          <!-- File Upload Zone -->
          <div
            class="upload-zone"
            :class="{ 'drag-over': isDragging }"
            @drop.prevent="handleFileDrop"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
          >
            <div class="upload-content">
              <svg class="upload-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <p class="upload-text">Drag & drop a decklist file here, or</p>
              <label class="btn btn-upload">
                Choose File
                <input
                  type="file"
                  ref="fileInput"
                  accept=".txt,.dek,.dec"
                  @change="handleFileSelect"
                  style="display: none"
                />
              </label>
              <p class="upload-hint">Supports .txt, .dek, .dec files</p>
            </div>
          </div>

          <div class="or-divider">
            <span>OR</span>
          </div>

          <textarea
            v-model="decklistText"
            rows="15"
            placeholder="Paste your decklist here (format: quantity card name, one per line)
Example:
4 Lightning Bolt
4 Monastery Swiftspear
20 Mountain"
            required
          ></textarea>
          <div class="help-actions">
            <p class="help-text">Enter one card per line in the format: quantity card name</p>
            <button type="button" @click="downloadExample" class="btn-link">
              Download Example Decklist
            </button>
          </div>
        </div>

        <div v-if="parseError" class="error">{{ parseError }}</div>

        <button type="submit" class="btn btn-primary" :disabled="submitting">
          {{ submitting ? 'Uploading...' : 'Upload Decklist' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useDecklistStore } from '../store'

const router = useRouter()
const decklistStore = useDecklistStore()

const form = ref({
  name: '',
  format: '',
  archetype: ''
})

const decklistText = ref('')
const parseError = ref('')
const submitting = ref(false)
const isDragging = ref(false)
const fileInput = ref(null)

const parseDecklist = () => {
  const lines = decklistText.value.split('\n').filter(line => line.trim())
  const cards = []
  parseError.value = ''

  for (const line of lines) {
    // Skip section headers (Deck, Sideboard, Companion, etc.)
    if (line.match(/^(Deck|Sideboard|Companion|Commander|Maindeck)/i)) {
      continue
    }

    // Skip empty lines and comments
    if (!line.trim() || line.trim().startsWith('//')) {
      continue
    }

    // Match various formats:
    // "4 Lightning Bolt" or "4x Lightning Bolt" or "Lightning Bolt x4"
    let match = line.trim().match(/^(\d+)x?\s+(.+)$/)

    if (!match) {
      // Try reverse format: "Card Name x4"
      match = line.trim().match(/^(.+?)\s+x(\d+)$/i)
      if (match) {
        const quantity = parseInt(match[2])
        const name = match[1].trim()
        cards.push({ quantity, name })
        continue
      }
    }

    if (!match) {
      // Try MTGO format with set codes: "4 [ZNR] Lightning Bolt"
      match = line.trim().match(/^(\d+)\s+\[[\w\d]+\]\s+(.+)$/)
    }

    if (!match) {
      parseError.value = `Invalid format: "${line}". Use format: quantity card name`
      return null
    }

    const quantity = parseInt(match[1])
    const name = match[2].trim()

    if (quantity <= 0) {
      parseError.value = `Invalid quantity for "${name}"`
      return null
    }

    cards.push({ quantity, name })
  }

  if (cards.length === 0) {
    parseError.value = 'Please add at least one card'
    return null
  }

  return cards
}

const handleFileSelect = async (event) => {
  const file = event.target.files[0]
  if (file) {
    await loadDecklistFromFile(file)
  }
}

const handleFileDrop = async (event) => {
  isDragging.value = false
  const file = event.dataTransfer.files[0]
  if (file) {
    await loadDecklistFromFile(file)
  }
}

const loadDecklistFromFile = async (file) => {
  try {
    const text = await file.text()
    decklistText.value = text
    parseError.value = ''

    // Try to extract deck name from filename if form name is empty
    if (!form.value.name) {
      const fileName = file.name.replace(/\.(txt|dek|dec)$/i, '')
      form.value.name = fileName
    }
  } catch (err) {
    parseError.value = 'Failed to read file. Please try again.'
  }
}

const downloadExample = () => {
  const exampleDecklist = `Mono Red Aggro - Modern

Deck
4 Goblin Guide
4 Monastery Swiftspear
4 Eidolon of the Great Revel
4 Lightning Bolt
4 Lava Spike
4 Rift Bolt
4 Skewer the Critics
4 Light Up the Stage
2 Searing Blaze
20 Mountain
4 Sunbaked Canyon
2 Fiery Islet

Sideboard
3 Leyline of the Void
2 Searing Blood
2 Deflecting Palm
4 Skullcrack
2 Roiling Vortex
2 Relic of Progenitus
`

  const blob = new Blob([exampleDecklist], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'example-decklist.txt'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const handleSubmit = async () => {
  const cards = parseDecklist()
  if (!cards) return

  submitting.value = true
  try {
    const decklist = await decklistStore.createDecklist({
      name: form.value.name,
      format: form.value.format,
      archetype: form.value.archetype || null,
      cards
    })

    router.push(`/decklists/${decklist._id}`)
  } catch (err) {
    parseError.value = err.response?.data?.message || 'Failed to upload decklist'
  }
  submitting.value = false
}
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

input, select, textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
}

textarea {
  font-family: 'Courier New', monospace;
  resize: vertical;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: #3498db;
}

.help-text {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #7f8c8d;
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

.upload-zone {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  background: #f8f9fa;
  transition: all 0.3s;
  margin-bottom: 1rem;
}

.upload-zone.drag-over {
  border-color: #3498db;
  background: #e3f2fd;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.upload-icon {
  width: 48px;
  height: 48px;
  color: #7f8c8d;
}

.upload-text {
  color: #7f8c8d;
  margin: 0;
}

.btn-upload {
  background: #3498db;
  cursor: pointer;
  display: inline-block;
  margin: 0;
}

.btn-upload:hover {
  background: #2980b9;
}

.upload-hint {
  font-size: 0.85rem;
  color: #95a5a6;
  margin: 0;
}

.or-divider {
  text-align: center;
  margin: 1.5rem 0;
  position: relative;
}

.or-divider::before {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  top: 50%;
  height: 1px;
  background: #ddd;
}

.or-divider span {
  background: white;
  padding: 0 1rem;
  position: relative;
  color: #7f8c8d;
  font-weight: 500;
}

.help-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
}

.btn-link {
  background: none;
  border: none;
  color: #3498db;
  cursor: pointer;
  font-size: 0.9rem;
  text-decoration: underline;
  padding: 0;
}

.btn-link:hover {
  color: #2980b9;
}
</style>
