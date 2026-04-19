import { apiClient } from '../../api/client'
import type { Booking, BookingPayload } from './types'

export async function fetchBookings() {
  const response = await apiClient.get<Booking[]>('/bookings')
  return response.data
}

export async function fetchBookingById(bookingId: number) {
  const response = await apiClient.get<Booking>(`/bookings/${bookingId}`)
  return response.data
}

export async function createBooking(payload: BookingPayload) {
  const response = await apiClient.post<Booking>('/bookings', payload)
  return response.data
}

export async function updateBooking(bookingId: number, payload: BookingPayload) {
  const response = await apiClient.put<Booking>(`/bookings/${bookingId}`, payload)
  return response.data
}

export async function cancelBooking(bookingId: number) {
  const response = await apiClient.post<Booking>(`/bookings/${bookingId}/cancel`)
  return response.data
}
