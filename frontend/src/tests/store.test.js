import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore, useDecklistStore, useScenarioStore } from '../store'
import api from '../api/client'

vi.mock('../api/client')

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
    vi.clearAllMocks()
  })

  it('initializes with no user and token from localStorage', () => {
    const store = useAuthStore()
    expect(store.user).toBeNull()
    expect(store.token).toBeNull()
    expect(store.isAuthenticated).toBe(false)
  })

  it('registers a user successfully', async () => {
    const mockResponse = {
      data: {
        token: 'test-token',
        user: { username: 'testuser', email: 'test@example.com' }
      }
    }

    api.auth.register.mockResolvedValue(mockResponse)

    const store = useAuthStore()
    await store.register('testuser', 'test@example.com', 'password')

    expect(store.token).toBe('test-token')
    expect(store.user.username).toBe('testuser')
    expect(store.isAuthenticated).toBe(true)
    expect(localStorage.getItem('token')).toBe('test-token')
  })

  it('logs in a user successfully', async () => {
    const mockResponse = {
      data: {
        token: 'login-token',
        user: { username: 'loginuser', email: 'login@example.com' }
      }
    }

    api.auth.login.mockResolvedValue(mockResponse)

    const store = useAuthStore()
    await store.login('login@example.com', 'password')

    expect(store.token).toBe('login-token')
    expect(store.user.username).toBe('loginuser')
    expect(store.isAuthenticated).toBe(true)
  })

  it('logs out a user', () => {
    const store = useAuthStore()
    store.token = 'test-token'
    store.user = { username: 'user' }

    store.logout()

    expect(store.token).toBeNull()
    expect(store.user).toBeNull()
    expect(store.isAuthenticated).toBe(false)
    expect(localStorage.getItem('token')).toBeNull()
  })
})

describe('Decklist Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('fetches all decklists', async () => {
    const mockDecklists = [
      { _id: '1', name: 'Deck 1' },
      { _id: '2', name: 'Deck 2' }
    ]

    api.decklists.getAll.mockResolvedValue({ data: { decklists: mockDecklists } })

    const store = useDecklistStore()
    await store.fetchDecklists()

    expect(store.decklists).toEqual(mockDecklists)
  })

  it('fetches user decklists', async () => {
    const mockDecklists = [{ _id: '1', name: 'My Deck' }]

    api.decklists.getMy.mockResolvedValue({ data: { decklists: mockDecklists } })

    const store = useDecklistStore()
    await store.fetchMyDecklists()

    expect(store.myDecklists).toEqual(mockDecklists)
  })

  it('creates a new decklist', async () => {
    const mockDecklist = { _id: '1', name: 'New Deck' }

    api.decklists.create.mockResolvedValue({ data: { decklist: mockDecklist } })

    const store = useDecklistStore()
    const result = await store.createDecklist({ name: 'New Deck', cards: [] })

    expect(result).toEqual(mockDecklist)
  })
})

describe('Scenario Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('fetches scenarios with pagination', async () => {
    const mockResponse = {
      data: {
        scenarios: [{ _id: '1' }],
        total: 10,
        page: 1,
        per_page: 20
      }
    }

    api.scenarios.getAll.mockResolvedValue(mockResponse)

    const store = useScenarioStore()
    await store.fetchScenarios(1)

    expect(store.scenarios).toEqual([{ _id: '1' }])
    expect(store.total).toBe(10)
    expect(store.page).toBe(1)
  })

  it('creates a vote on a scenario', async () => {
    api.votes.create.mockResolvedValue({ data: {} })
    api.scenarios.getById.mockResolvedValue({
      data: { scenario: { _id: '1', keep_votes: 1 } }
    })

    const store = useScenarioStore()
    store.currentScenario = { _id: '1', keep_votes: 0 }

    await store.vote('1', 'keep')

    expect(api.votes.create).toHaveBeenCalledWith('1', 'keep')
  })

  it('gets user vote for a scenario', async () => {
    const mockVote = { decision: 'keep' }
    api.votes.getUserVote.mockResolvedValue({ data: { vote: mockVote } })

    const store = useScenarioStore()
    const result = await store.getUserVote('scenario-id')

    expect(result).toEqual(mockVote)
  })
})
