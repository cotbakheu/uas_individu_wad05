import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

import { api, setCsrfToken } from '@/services/api'
import type { User } from '@/types'

type AuthResponse = { user: User; csrf_token: string }

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const loading = ref(false)
  const initialized = ref(false)
  const isAuthenticated = computed(() => user.value !== null)

  async function restore() {
    if (initialized.value) return
    try {
      const response = await api.get<AuthResponse>('/auth/me')
      user.value = response.user
      setCsrfToken(response.csrf_token)
    } catch {
      user.value = null
    } finally {
      initialized.value = true
    }
  }

  async function login(email: string, password: string) {
    loading.value = true
    try {
      const response = await api.post<AuthResponse>('/auth/login', { email, password })
      user.value = response.user
      setCsrfToken(response.csrf_token)
    } finally {
      loading.value = false
    }
  }

  async function register(name: string, email: string, password: string) {
    loading.value = true
    try {
      const response = await api.post<AuthResponse>('/auth/register', { name, email, password })
      user.value = response.user
      setCsrfToken(response.csrf_token)
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    loading.value = true
    try {
      await api.post('/auth/logout')
      user.value = null
      setCsrfToken('')
    } finally {
      loading.value = false
    }
  }

  return { user, loading, initialized, isAuthenticated, restore, login, register, logout }
})
