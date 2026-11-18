import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { api, setAuthToken, setUnauthorizedHandler } from '@/lib/api'
import { readStorage, writeStorage } from '@/lib/storage'

const TOKEN_KEY = 'shefa-mini.token'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(readStorage(TOKEN_KEY))
  const user = ref(null)
  const ready = ref(false)

  setAuthToken(token.value)

  const isAuthenticated = computed(() => Boolean(token.value))
  const balance = computed(() => user.value?.balance ?? '0.00')
  const firstName = computed(() => user.value?.name?.split(' ')[0] ?? '')

  function startSession(payload) {
    token.value = payload.token
    user.value = payload.user
    setAuthToken(payload.token)
    writeStorage(TOKEN_KEY, payload.token)
  }

  function clearSession() {
    token.value = null
    user.value = null
    setAuthToken(null)
    writeStorage(TOKEN_KEY, null)
  }

  setUnauthorizedHandler(clearSession)

  async function init() {
    if (ready.value) return
    if (token.value) {
      try {
        user.value = await api.me()
      } catch (error) {
        if (error.status === 401) clearSession()
      }
    }
    ready.value = true
  }

  async function signup(form) {
    startSession(await api.signup(form))
  }

  async function login(form) {
    startSession(await api.login(form))
  }

  async function logout() {
    try {
      await api.logout()
    } catch {
      // the token is dropped locally either way
    }
    clearSession()
  }

  async function refresh() {
    if (!token.value) return
    user.value = await api.me()
  }

  function setBalance(value) {
    if (user.value) user.value = { ...user.value, balance: String(value) }
  }

  async function updateName(name) {
    user.value = await api.updateMe({ name })
  }

  return {
    token,
    user,
    ready,
    isAuthenticated,
    balance,
    firstName,
    init,
    signup,
    login,
    logout,
    refresh,
    setBalance,
    updateName,
  }
})
