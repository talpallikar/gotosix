import axios from 'axios'

const SCRYFALL_API_BASE = 'https://api.scryfall.com'

// Cache to avoid repeated API calls for the same card
const cardCache = new Map()

export default {
  /**
   * Search for a card by exact name
   * @param {string} cardName - The exact name of the card
   * @returns {Promise} Card data from Scryfall
   */
  async getCardByName(cardName) {
    // Check cache first
    if (cardCache.has(cardName)) {
      return cardCache.get(cardName)
    }

    try {
      // Use fuzzy search endpoint which is more forgiving
      const response = await axios.get(`${SCRYFALL_API_BASE}/cards/named`, {
        params: {
          fuzzy: cardName
        }
      })

      const cardData = response.data
      cardCache.set(cardName, cardData)
      return cardData
    } catch (error) {
      console.error(`Failed to fetch card: ${cardName}`, error)
      return null
    }
  },

  /**
   * Get multiple cards by name
   * @param {Array<string>} cardNames - Array of card names
   * @returns {Promise<Array>} Array of card data
   */
  async getCardsByNames(cardNames) {
    const uniqueNames = [...new Set(cardNames)]
    const promises = uniqueNames.map(name => this.getCardByName(name))
    return Promise.all(promises)
  },

  /**
   * Get the image URL for a card
   * @param {Object} card - Card data from Scryfall
   * @param {string} size - Image size: small, normal, large, png, art_crop, border_crop
   * @returns {string} Image URL
   */
  getCardImageUrl(card, size = 'normal') {
    if (!card || !card.image_uris) {
      // Handle double-faced cards
      if (card && card.card_faces && card.card_faces[0].image_uris) {
        return card.card_faces[0].image_uris[size] || card.card_faces[0].image_uris.normal
      }
      return null
    }
    return card.image_uris[size] || card.image_uris.normal
  },

  /**
   * Clear the cache (useful for testing or memory management)
   */
  clearCache() {
    cardCache.clear()
  }
}
