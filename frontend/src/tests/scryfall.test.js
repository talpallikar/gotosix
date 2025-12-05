import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import axios from 'axios'
import scryfallApi from '../api/scryfall'

vi.mock('axios')

describe('Scryfall API Client', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    scryfallApi.clearCache()
  })

  describe('getCardByName', () => {
    it('fetches card data from Scryfall API', async () => {
      const mockCardData = {
        name: 'Lightning Bolt',
        image_uris: {
          normal: 'https://example.com/card.jpg'
        }
      }

      axios.get.mockResolvedValue({ data: mockCardData })

      const result = await scryfallApi.getCardByName('Lightning Bolt')

      expect(axios.get).toHaveBeenCalledWith(
        'https://api.scryfall.com/cards/named',
        { params: { fuzzy: 'Lightning Bolt' } }
      )
      expect(result).toEqual(mockCardData)
    })

    it('returns cached data on second request', async () => {
      const mockCardData = {
        name: 'Lightning Bolt',
        image_uris: { normal: 'https://example.com/card.jpg' }
      }

      axios.get.mockResolvedValue({ data: mockCardData })

      // First call
      await scryfallApi.getCardByName('Lightning Bolt')

      // Second call should use cache
      const result = await scryfallApi.getCardByName('Lightning Bolt')

      expect(axios.get).toHaveBeenCalledTimes(1)
      expect(result).toEqual(mockCardData)
    })

    it('returns null on error', async () => {
      axios.get.mockRejectedValue(new Error('Card not found'))

      const result = await scryfallApi.getCardByName('Invalid Card')

      expect(result).toBeNull()
    })
  })

  describe('getCardsByNames', () => {
    it('fetches multiple cards', async () => {
      const mockCard1 = { name: 'Card 1' }
      const mockCard2 = { name: 'Card 2' }

      axios.get
        .mockResolvedValueOnce({ data: mockCard1 })
        .mockResolvedValueOnce({ data: mockCard2 })

      const results = await scryfallApi.getCardsByNames(['Card 1', 'Card 2'])

      expect(results).toHaveLength(2)
      expect(axios.get).toHaveBeenCalledTimes(2)
    })

    it('handles duplicate card names', async () => {
      const mockCard = { name: 'Card 1' }

      axios.get.mockResolvedValue({ data: mockCard })

      const results = await scryfallApi.getCardsByNames(['Card 1', 'Card 1', 'Card 1'])

      expect(results).toHaveLength(1)
      expect(axios.get).toHaveBeenCalledTimes(1)
    })
  })

  describe('getCardImageUrl', () => {
    it('returns normal image URL by default', () => {
      const card = {
        image_uris: {
          small: 'small.jpg',
          normal: 'normal.jpg',
          large: 'large.jpg'
        }
      }

      const url = scryfallApi.getCardImageUrl(card)

      expect(url).toBe('normal.jpg')
    })

    it('returns specified size image URL', () => {
      const card = {
        image_uris: {
          small: 'small.jpg',
          normal: 'normal.jpg',
          large: 'large.jpg'
        }
      }

      const url = scryfallApi.getCardImageUrl(card, 'large')

      expect(url).toBe('large.jpg')
    })

    it('handles double-faced cards', () => {
      const card = {
        card_faces: [
          {
            image_uris: {
              normal: 'front.jpg'
            }
          }
        ]
      }

      const url = scryfallApi.getCardImageUrl(card)

      expect(url).toBe('front.jpg')
    })

    it('returns null for card without images', () => {
      const card = { name: 'Card' }

      const url = scryfallApi.getCardImageUrl(card)

      expect(url).toBeNull()
    })
  })

  describe('clearCache', () => {
    it('clears the card cache', async () => {
      const mockCardData = { name: 'Card' }
      axios.get.mockResolvedValue({ data: mockCardData })

      // Fetch a card
      await scryfallApi.getCardByName('Card')
      expect(axios.get).toHaveBeenCalledTimes(1)

      // Clear cache
      scryfallApi.clearCache()

      // Fetch again - should make new request
      await scryfallApi.getCardByName('Card')
      expect(axios.get).toHaveBeenCalledTimes(2)
    })
  })
})
