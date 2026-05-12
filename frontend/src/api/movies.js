import api from './client'

export async function fetchMovies(params = {}) {
  const { data } = await api.get('/movies', { params })
  return data
}

export async function fetchMovieMeta() {
  const { data } = await api.get('/movies/meta')
  return data
}

export async function fetchRecommendations(city = '') {
  const { data } = await api.get('/movies/recommendations', { params: { city } })
  return data
}

export async function fetchMovieDetails(movieId) {
  const { data } = await api.get(`/movies/${movieId}`)
  return data
}

export async function fetchSearchSuggestions(query) {
  const { data } = await api.get('/search/suggestions', { params: { q: query } })
  return data
}

export async function fetchSeatMap(showId) {
  const { data } = await api.get(`/shows/${showId}/seats`)
  return data
}
