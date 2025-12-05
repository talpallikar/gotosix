import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default {
  auth: {
    register(username, email, password) {
      return apiClient.post('/auth/register', { username, email, password })
    },
    login(email, password) {
      return apiClient.post('/auth/login', { email, password })
    }
  },

  decklists: {
    getAll() {
      return apiClient.get('/decklists')
    },
    getById(id) {
      return apiClient.get(`/decklists/${id}`)
    },
    getMy() {
      return apiClient.get('/decklists/my')
    },
    create(decklist) {
      return apiClient.post('/decklists', decklist)
    }
  },

  scenarios: {
    getAll(page = 1, perPage = 20) {
      return apiClient.get('/scenarios', { params: { page, per_page: perPage } })
    },
    getById(id) {
      return apiClient.get(`/scenarios/${id}`)
    },
    create(scenario) {
      return apiClient.post('/scenarios', scenario)
    }
  },

  votes: {
    create(scenarioId, decision) {
      return apiClient.post('/votes', { scenario_id: scenarioId, decision })
    },
    getUserVote(scenarioId) {
      return apiClient.get(`/votes/scenario/${scenarioId}`)
    }
  }
}
