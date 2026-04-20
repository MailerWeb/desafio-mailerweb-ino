import { apiClient } from '../../api/client'
import type { CreateRoomPayload, Room } from './types'

export async function fetchRooms() {
  const response = await apiClient.get<Room[]>('/rooms')
  return response.data
}

export async function createRoom(payload: CreateRoomPayload) {
  const response = await apiClient.post<Room>('/rooms', payload)
  return response.data
}
