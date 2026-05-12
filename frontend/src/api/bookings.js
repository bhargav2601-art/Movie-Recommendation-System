import api from './client'

export async function createBooking(payload) {
  const { data } = await api.post('/bookings', payload)
  return data
}

export async function fetchMyBookings() {
  const { data } = await api.get('/bookings/me')
  return data
}
