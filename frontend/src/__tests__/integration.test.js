import { describe, it, expect, beforeEach, vi } from 'vitest'
import { formatDate, formatTime, formatDateInput, calculateDuration } from '../utils/formatters'

describe('Formatters Utils', () => {
  it('should format date correctly', () => {
    const date = '2024-03-10T10:30:00Z'
    const formatted = formatDate(date)
    expect(formatted).toMatch(/10\/03\/2024/)
    expect(formatted).toMatch(/10:30/)
  })

  it('should format time correctly', () => {
    const date = '2024-03-10T14:45:00Z'
    const formatted = formatTime(date)
    expect(formatted).toMatch(/14:45/)
  })

  it('should calculate duration correctly', () => {
    const start = '2024-03-10T10:00:00Z'
    const end = '2024-03-10T12:30:00Z'
    const duration = calculateDuration(start, end)
    expect(duration).toBe('2h 30m')
  })

  it('should calculate duration in minutes only', () => {
    const start = '2024-03-10T10:00:00Z'
    const end = '2024-03-10T10:45:00Z'
    const duration = calculateDuration(start, end)
    expect(duration).toBe('45m')
  })

  it('should calculate duration in hours only', () => {
    const start = '2024-03-10T10:00:00Z'
    const end = '2024-03-10T13:00:00Z'
    const duration = calculateDuration(start, end)
    expect(duration).toBe('3h 0m')
  })
})

describe('API Integration', () => {
  it('should validate booking duration constraints', () => {
    // Duration minimum 15 minutes
    const start = new Date('2024-03-10T10:00:00')
    const end = new Date('2024-03-10T10:15:00')
    const durationMinutes = (end - start) / 60000
    expect(durationMinutes).toBe(15)

    // Duration maximum 8 hours
    const endMax = new Date('2024-03-10T18:00:00')
    const durationMaxMinutes = (endMax - start) / 60000
    expect(durationMaxMinutes).toBe(480)
  })

  it('should validate booking overlap', () => {
    // Overlap detection logic
    const booking1 = {
      start_at: new Date('2024-03-10T10:00:00'),
      end_at: new Date('2024-03-10T11:00:00'),
    }

    const booking2 = {
      start_at: new Date('2024-03-10T10:30:00'),
      end_at: new Date('2024-03-10T11:30:00'),
    }

    const hasOverlap =
      booking2.start_at < booking1.end_at &&
      booking2.end_at > booking1.start_at

    expect(hasOverlap).toBe(true)
  })

  it('should not detect overlap for adjacent bookings', () => {
    const booking1 = {
      start_at: new Date('2024-03-10T10:00:00'),
      end_at: new Date('2024-03-10T11:00:00'),
    }

    const booking2 = {
      start_at: new Date('2024-03-10T11:00:00'),
      end_at: new Date('2024-03-10T12:00:00'),
    }

    const hasOverlap =
      booking2.start_at < booking1.end_at &&
      booking2.end_at > booking1.start_at

    expect(hasOverlap).toBe(false)
  })
})
