// Thin fetch wrapper for the Django API. Errors come back as ApiError with field messages.

const API_URL = (import.meta.env.VITE_API_URL ?? '').replace(/\/+$/, '')

let authToken = null

export function setAuthToken(token) {
  authToken = token || null
}

let onUnauthorized = () => {}

export function setUnauthorizedHandler(handler) {
  onUnauthorized = handler
}

export class ApiError extends Error {
  constructor(status, body) {
    super(messageFrom(status, body))
    this.name = 'ApiError'
    this.status = status
    this.body = body || {}
    this.code = typeof this.body.code === 'string' ? this.body.code : null
    this.fields = fieldErrors(this.body)
  }
}

function fieldErrors(body) {
  const fields = {}
  if (!body || typeof body !== 'object') return fields
  for (const [key, value] of Object.entries(body)) {
    if (['detail', 'code', 'status', 'non_field_errors'].includes(key)) continue
    fields[key] = Array.isArray(value) ? value.join(' ') : String(value)
  }
  return fields
}

function messageFrom(status, body) {
  if (body?.detail) return String(body.detail)
  if (body?.non_field_errors) return [].concat(body.non_field_errors).join(' ')
  if (status === 0) return 'Cannot reach the server. Check your connection and try again.'
  if (status === 429) return 'Too many attempts. Please wait a minute and try again.'
  if (status >= 500) return 'Something went wrong on our side. Please try again.'
  if (body && typeof body === 'object' && Object.keys(body).length) {
    return 'Please check the highlighted fields.'
  }
  return 'The request failed. Please try again.'
}

export async function request(path, { method = 'GET', body, query } = {}) {
  let url = `${API_URL}/api${path}`
  if (query) {
    const params = new URLSearchParams()
    for (const [k, v] of Object.entries(query)) {
      if (v !== undefined && v !== null && v !== '') params.set(k, v)
    }
    const qs = params.toString()
    if (qs) url += `?${qs}`
  }

  const headers = { Accept: 'application/json' }
  if (body !== undefined) headers['Content-Type'] = 'application/json'
  if (authToken) headers.Authorization = `Token ${authToken}`

  let response
  try {
    response = await fetch(url, {
      method,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    })
  } catch {
    throw new ApiError(0, null)
  }

  if (response.status === 204) return null
  let data = null
  const text = await response.text()
  if (text) {
    try {
      data = JSON.parse(text)
    } catch {
      data = null
    }
  }
  if (!response.ok) {
    if (response.status === 401 && authToken) onUnauthorized()
    throw new ApiError(response.status, data)
  }
  return data
}

export const api = {
  health: () => request('/health/'),

  signup: (payload) => request('/auth/signup/', { method: 'POST', body: payload }),
  login: (payload) => request('/auth/login/', { method: 'POST', body: payload }),
  logout: () => request('/auth/logout/', { method: 'POST' }),
  me: () => request('/auth/me/'),
  updateMe: (payload) => request('/auth/me/', { method: 'PATCH', body: payload }),

  wallet: () => request('/wallet/'),
  transactions: (page = 1) => request('/wallet/transactions/', { query: { page } }),
  topUp: (payload) => request('/wallet/top-up/', { method: 'POST', body: payload }),

  cases: (filters = {}) => request('/cases/', { query: filters }),
  caseSummary: () => request('/cases/summary/'),
  caseDetail: (slug) => request(`/cases/${encodeURIComponent(slug)}/`),
  donate: (slug, payload) =>
    request(`/cases/${encodeURIComponent(slug)}/donate/`, { method: 'POST', body: payload }),
  receipt: (reference) => request(`/donations/${encodeURIComponent(reference)}/`),
}
