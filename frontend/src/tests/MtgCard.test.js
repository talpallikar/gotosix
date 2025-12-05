import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import MtgCard from '../components/MtgCard.vue'
import scryfallApi from '../api/scryfall'

vi.mock('../api/scryfall')

describe('MtgCard', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders loading state initially', () => {
    scryfallApi.getCardByName.mockResolvedValue(null)

    const wrapper = mount(MtgCard, {
      props: {
        cardName: 'Lightning Bolt'
      }
    })

    expect(wrapper.find('.card-loading').exists()).toBe(true)
    expect(wrapper.text()).toContain('Lightning Bolt')
  })

  it('displays card image when loaded successfully', async () => {
    const mockCard = {
      image_uris: {
        normal: 'https://example.com/card.jpg'
      }
    }

    scryfallApi.getCardByName.mockResolvedValue(mockCard)
    scryfallApi.getCardImageUrl.mockReturnValue('https://example.com/card.jpg')

    const wrapper = mount(MtgCard, {
      props: {
        cardName: 'Lightning Bolt'
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(scryfallApi.getCardByName).toHaveBeenCalledWith('Lightning Bolt')
  })

  it('displays error state when card not found', async () => {
    scryfallApi.getCardByName.mockResolvedValue(null)

    const wrapper = mount(MtgCard, {
      props: {
        cardName: 'Invalid Card'
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(wrapper.find('.card-error').exists()).toBe(true)
  })

  it('uses correct image size from props', async () => {
    const mockCard = {
      image_uris: {
        small: 'https://example.com/card-small.jpg',
        normal: 'https://example.com/card-normal.jpg',
        large: 'https://example.com/card-large.jpg'
      }
    }

    scryfallApi.getCardByName.mockResolvedValue(mockCard)
    scryfallApi.getCardImageUrl.mockReturnValue('https://example.com/card-small.jpg')

    const wrapper = mount(MtgCard, {
      props: {
        cardName: 'Lightning Bolt',
        size: 'small'
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(scryfallApi.getCardImageUrl).toHaveBeenCalledWith(mockCard, 'small')
  })

  it('shows card name overlay when showName is true', async () => {
    const mockCard = {
      image_uris: {
        normal: 'https://example.com/card.jpg'
      }
    }

    scryfallApi.getCardByName.mockResolvedValue(mockCard)
    scryfallApi.getCardImageUrl.mockReturnValue('https://example.com/card.jpg')

    const wrapper = mount(MtgCard, {
      props: {
        cardName: 'Lightning Bolt',
        showName: true
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))

    expect(wrapper.html()).toContain('Lightning Bolt')
  })
})
