import api from './api'

export const authService = {
  async register(name, email, password) {
    const response = await api.post('/users/register', {
      name,
      email,
      password,
    })
    return response.data.data
  },

  async login(email, password) {
    const response = await api.post('/users/login', {
      email,
      password,
    })
    const token = response.data.data.access_token
    localStorage.setItem('token', token)
    return token
  },

  async getUserInfo(userId) {
    const response = await api.get(`/users/${userId}`)
    return response.data.data
  },

  logout() {
    localStorage.removeItem('token')
  },

  getToken() {
    return localStorage.getItem('token')
  },

  isAuthenticated() {
    return !!localStorage.getItem('token')
  },
}

export const roomService = {
  async listRooms() {
    const response = await api.get('/rooms/')
    return response.data.data
  },

  async getRoomById(roomId) {
    const response = await api.get(`/rooms/${roomId}`)
    return response.data.data
  },

  async createRoom(name, capacity) {
    const response = await api.post('/rooms/', {
      name,
      capacity,
    })
    return response.data.data
  },
}

export const bookingService = {
  async listBookings() {
    const response = await api.get('/bookings/')
    return response.data.data
  },

  async getBookingById(bookingId) {
    const response = await api.get(`/bookings/${bookingId}`)
    return response.data.data
  },

  async createBooking(title, roomId, startAt, endAt, participants) {
    const response = await api.post('/bookings/', {
      title,
      room_id: roomId,
      start_at: startAt,
      end_at: endAt,
      participants,
    })
    return response.data.data
  },

  async updateBooking(bookingId, title, startAt, endAt, participants) {
    const response = await api.put(`/bookings/${bookingId}`, {
      title,
      start_at: startAt,
      end_at: endAt,
      participants,
    })
    return response.data.data
  },

  async cancelBooking(bookingId) {
    const response = await api.delete(`/bookings/${bookingId}`)
    return response.data.data
  },
}
