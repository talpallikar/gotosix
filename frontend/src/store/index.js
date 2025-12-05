import { defineStore } from 'pinia'
import api from '../api/client'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token
  },

  actions: {
    async register(username, email, password) {
      const response = await api.auth.register(username, email, password)
      this.token = response.data.token
      this.user = response.data.user
      localStorage.setItem('token', this.token)
      return response.data
    },

    async login(email, password) {
      const response = await api.auth.login(email, password)
      this.token = response.data.token
      this.user = response.data.user
      localStorage.setItem('token', this.token)
      return response.data
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    }
  }
})

export const useDecklistStore = defineStore('decklist', {
  state: () => ({
    decklists: [],
    myDecklists: [],
    currentDecklist: null
  }),

  actions: {
    async fetchDecklists() {
      const response = await api.decklists.getAll()
      this.decklists = response.data.decklists
    },

    async fetchMyDecklists() {
      const response = await api.decklists.getMy()
      this.myDecklists = response.data.decklists
    },

    async fetchDecklist(id) {
      const response = await api.decklists.getById(id)
      this.currentDecklist = response.data.decklist
    },

    async createDecklist(decklist) {
      const response = await api.decklists.create(decklist)
      return response.data.decklist
    }
  }
})

export const useScenarioStore = defineStore('scenario', {
  state: () => ({
    scenarios: [],
    currentScenario: null,
    total: 0,
    page: 1,
    perPage: 20
  }),

  actions: {
    async fetchScenarios(page = 1) {
      const response = await api.scenarios.getAll(page, this.perPage)
      this.scenarios = response.data.scenarios
      this.total = response.data.total
      this.page = response.data.page
    },

    async fetchScenario(id) {
      const response = await api.scenarios.getById(id)
      this.currentScenario = response.data.scenario
    },

    async createScenario(scenario) {
      const response = await api.scenarios.create(scenario)
      return response.data.scenario
    },

    async vote(scenarioId, decision) {
      await api.votes.create(scenarioId, decision)
      if (this.currentScenario && this.currentScenario._id === scenarioId) {
        await this.fetchScenario(scenarioId)
      }
    },

    async getUserVote(scenarioId) {
      const response = await api.votes.getUserVote(scenarioId)
      return response.data.vote
    }
  }
})
