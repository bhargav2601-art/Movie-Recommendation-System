import api from './client'

export async function signup(payload) {
  const { data } = await api.post('/auth/signup', payload)
  return data
}

export async function loginUser(payload) {
  const { data } = await api.post('/auth/login/user', payload)
  return data
}

export async function loginAdmin(payload) {
  const { data } = await api.post('/auth/login/admin', payload)
  return data
}

export async function logout() {
  const { data } = await api.post('/auth/logout')
  return data
}
