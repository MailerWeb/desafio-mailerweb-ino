import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import BookingList from '../pages/BookingList'
import * as authService from '../services/auth'

vi.mock('../services/auth')
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom')
  return {
    ...actual,
    useNavigate: () => vi.fn(),
  }
})

describe('BookingList Component', () => {
  const mockBookings = [
    {
      id: '1',
      title: 'Reunião 1',
      room_id: 'room-1',
      start_at: '2024-03-10T10:00:00Z',
      end_at: '2024-03-10T11:00:00Z',
      status: 'active',
      participants: ['user1@example.com'],
    },
    {
      id: '2',
      title: 'Reunião 2',
      room_id: 'room-2',
      start_at: '2024-03-11T14:00:00Z',
      end_at: '2024-03-11T15:00:00Z',
      status: 'cancelled',
      participants: [],
    },
  ]

  beforeEach(() => {
    vi.clearAllMocks()
    authService.bookingService.listBookings.mockResolvedValue(mockBookings)
    authService.bookingService.cancelBooking.mockResolvedValue({})
  })

  it('renders loading state initially', () => {
    authService.bookingService.listBookings.mockImplementation(
      () =>
        new Promise(() => {
          /* never resolves */
        })
    )

    render(
      <BrowserRouter>
        <BookingList />
      </BrowserRouter>
    )

    expect(screen.getByRole('img', { hidden: true })).toBeInTheDocument()
  })

  it('renders bookings after loading', async () => {
    render(
      <BrowserRouter>
        <BookingList />
      </BrowserRouter>
    )

    await waitFor(() => {
      expect(screen.getByText('Reunião 1')).toBeInTheDocument()
      expect(screen.getByText('Reunião 2')).toBeInTheDocument()
    })
  })

  it('filters bookings by status', async () => {
    render(
      <BrowserRouter>
        <BookingList />
      </BrowserRouter>
    )

    await waitFor(() => {
      expect(screen.getByText('Reunião 1')).toBeInTheDocument()
    })

    const activeButton = screen.getByRole('button', { name: /ativas/i })
    fireEvent.click(activeButton)

    expect(screen.getByText('Reunião 1')).toBeInTheDocument()
    expect(screen.queryByText('Reunião 2')).not.toBeInTheDocument()
  })

  it('calls cancelBooking when delete button is clicked', async () => {
    render(
      <BrowserRouter>
        <BookingList />
      </BrowserRouter>
    )

    await waitFor(() => {
      expect(screen.getByText('Reunião 1')).toBeInTheDocument()
    })

    const cancelButtons = screen.getAllByRole('button', { name: /cancelar/i })
    fireEvent.click(cancelButtons[0])

    // Simulate confirm dialog
    window.confirm = vi.fn(() => true)

    await waitFor(() => {
      expect(authService.bookingService.cancelBooking).toHaveBeenCalled()
    })
  })
})
