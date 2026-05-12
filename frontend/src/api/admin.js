import api from './client'

export async function fetchAdminAnalytics() {
  const { data } = await api.get('/admin/analytics')
  return data
}

export async function fetchAdminCatalog() {
  const { data } = await api.get('/admin/catalog')
  return data
}

export async function createAdminMovie(payload) {
  const { data } = await api.post('/admin/movies', payload)
  return data
}

export async function archiveAdminMovie(movieId) {
  const { data } = await api.delete(`/admin/movies/${movieId}`)
  return data
}

export async function createAdminShow(payload) {
  const { data } = await api.post('/admin/shows', payload)
  return data
}

export async function createAdminTheater(payload) {
  const { data } = await api.post('/admin/theaters', payload)
  return data
}

export async function createAdminScreen(payload) {
  const { data } = await api.post('/admin/screens', payload)
  return data
}
