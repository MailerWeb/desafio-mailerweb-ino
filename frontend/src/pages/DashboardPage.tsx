import { useEffect, useMemo, useState } from 'react'
import axios from 'axios'
import { Link } from 'react-router-dom'
import { fetchBookings } from '../features/bookings/bookingsApi'
import type { Booking } from '../features/bookings/types'
import { fetchRooms } from '../features/rooms/roomsApi'
import type { Room } from '../features/rooms/types'

type DashboardTab = 'rooms' | 'bookings'

function getDashboardErrorMessage(error: unknown) {
  if (axios.isAxiosError(error)) {
    return (
      error.response?.data?.detail ??
      'Não foi possível carregar os dados do painel.'
    )
  }

  return 'Não foi possível carregar os dados do painel.'
}

function formatShortDate(dateValue: string) {
  return new Intl.DateTimeFormat('pt-BR', {
    dateStyle: 'short',
  }).format(new Date(dateValue))
}

function formatShortDateTime(dateValue: string) {
  return new Intl.DateTimeFormat('pt-BR', {
    dateStyle: 'short',
    timeStyle: 'short',
  }).format(new Date(dateValue))
}

function cn(...parts: Array<string | false>) {
  return parts.filter(Boolean).join(' ')
}

export function DashboardPage() {
  const [rooms, setRooms] = useState<Room[]>([])
  const [bookings, setBookings] = useState<Booking[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [activeTab, setActiveTab] = useState<DashboardTab>('rooms')

  useEffect(() => {
    let isMounted = true

    Promise.all([fetchRooms(), fetchBookings()])
      .then(([roomsResponse, bookingsResponse]) => {
        if (!isMounted) return
        setRooms(roomsResponse)
        setBookings(bookingsResponse)
        setError('')
      })
      .catch((requestError) => {
        if (!isMounted) return
        setError(getDashboardErrorMessage(requestError))
      })
      .finally(() => {
        if (!isMounted) return
        setIsLoading(false)
      })

    return () => {
      isMounted = false
    }
  }, [])

  const roomNameById = useMemo(
    () => new Map(rooms.map((room) => [room.id, room.name])),
    [rooms],
  )

  const metricCards = useMemo(() => {
    const activeBookings = bookings.filter((booking) => booking.status === 'ACTIVE')
    const canceledBookings = bookings.filter(
      (booking) => booking.status === 'CANCELED',
    )

    return [
      { label: 'Salas', value: rooms.length },
      { label: 'Reservas', value: bookings.length },
      { label: 'Ativas', value: activeBookings.length },
      { label: 'Canceladas', value: canceledBookings.length },
    ]
  }, [bookings, rooms.length])

  const visibleRooms = useMemo(
    () =>
      [...rooms]
        .sort((firstRoom, secondRoom) =>
          firstRoom.name.localeCompare(secondRoom.name, 'pt-BR'),
        )
        .slice(0, 8),
    [rooms],
  )

  const visibleBookings = useMemo(
    () =>
      [...bookings]
        .sort(
          (firstBooking, secondBooking) =>
            new Date(secondBooking.start_at).getTime() -
            new Date(firstBooking.start_at).getTime(),
        )
        .slice(0, 8),
    [bookings],
  )

  return (
    <section className="space-y-4">
      <section className="rounded-panel border border-app-border bg-white/90 p-4 shadow-soft">
        <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
          <div className="space-y-1">
            <span className="inline-flex rounded-full bg-app-muted px-3 py-1 text-xs font-medium text-app-strong">
              Dashboard
            </span>
            <h2 className="text-3xl font-semibold tracking-tight text-app-strong">
              Visão geral
            </h2>
          </div>

          <div className="flex flex-wrap gap-2">
            <Link
              className="inline-flex min-h-10 items-center justify-center rounded-xl border border-app-border px-4 text-sm font-medium text-app-strong transition-colors hover:bg-app-muted"
              to="/rooms"
            >
              Criar sala
            </Link>
            <Link
              className="inline-flex min-h-10 items-center justify-center rounded-xl bg-app-strong px-4 text-sm font-medium text-white transition-colors hover:bg-black"
              to="/bookings/new"
            >
              Criar reserva
            </Link>
            <Link
              className="inline-flex min-h-10 items-center justify-center rounded-xl border border-app-border px-4 text-sm font-medium text-app-strong transition-colors hover:bg-app-muted"
              to="/bookings"
            >
              Ver reservas
            </Link>
          </div>
        </div>

        {isLoading ? (
          <div className="mt-4 rounded-2xl border border-app-border bg-app-muted/80 p-4">
            <strong className="block text-sm font-medium text-app-strong">
              Carregando painel...
            </strong>
          </div>
        ) : null}

        {!isLoading && error ? (
          <div
            className="mt-4 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
            role="alert"
          >
            {error}
          </div>
        ) : null}

        {!isLoading && !error ? (
          <>
            <section className="mt-4 grid gap-3 md:grid-cols-4">
              {metricCards.map((card) => (
                <article
                  className="rounded-2xl border border-app-border bg-app-surface p-4"
                  key={card.label}
                >
                  <span className="text-xs font-medium uppercase tracking-[0.08em] text-app-soft">
                    {card.label}
                  </span>
                  <strong className="mt-3 block text-4xl font-semibold tracking-tight text-app-strong">
                    {card.value}
                  </strong>
                </article>
              ))}
            </section>

            <section className="mt-4 rounded-2xl border border-app-border bg-app-surface">
              <div className="flex items-center justify-between gap-4 border-b border-app-border px-4 py-3">
                <div
                  className="inline-flex rounded-full bg-app-muted p-1"
                  role="tablist"
                  aria-label="Listagens"
                >
                  <button
                    type="button"
                    role="tab"
                    aria-selected={activeTab === 'rooms'}
                    className={cn(
                      'min-h-9 rounded-full px-4 text-sm font-medium transition-colors',
                      activeTab === 'rooms'
                        ? 'bg-app-strong text-white'
                        : 'text-app-text hover:text-app-strong',
                    )}
                    onClick={() => setActiveTab('rooms')}
                  >
                    Salas
                  </button>
                  <button
                    type="button"
                    role="tab"
                    aria-selected={activeTab === 'bookings'}
                    className={cn(
                      'min-h-9 rounded-full px-4 text-sm font-medium transition-colors',
                      activeTab === 'bookings'
                        ? 'bg-app-strong text-white'
                        : 'text-app-text hover:text-app-strong',
                    )}
                    onClick={() => setActiveTab('bookings')}
                  >
                    Reservas
                  </button>
                </div>
              </div>

              {activeTab === 'rooms' ? (
                visibleRooms.length > 0 ? (
                  <div className="overflow-x-auto">
                    <table className="min-w-full border-collapse">
                      <thead>
                        <tr className="text-left">
                          <th className="px-4 py-3 text-xs font-medium uppercase tracking-[0.08em] text-app-soft">
                            Sala
                          </th>
                          <th className="px-4 py-3 text-xs font-medium uppercase tracking-[0.08em] text-app-soft">
                            Capacidade
                          </th>
                          <th className="px-4 py-3 text-xs font-medium uppercase tracking-[0.08em] text-app-soft">
                            Atualizada em
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {visibleRooms.map((room) => (
                          <tr className="border-t border-app-border" key={room.id}>
                            <td className="px-4 py-3 text-sm font-medium text-app-strong">
                              {room.name}
                            </td>
                            <td className="px-4 py-3 text-sm text-app-text">
                              {room.capacity} lugares
                            </td>
                            <td className="px-4 py-3 text-sm text-app-text">
                              {formatShortDate(room.updated_at)}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <div className="px-4 py-6 text-center text-sm text-app-text">
                    Nenhuma sala encontrada.
                  </div>
                )
              ) : visibleBookings.length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="min-w-full border-collapse">
                    <thead>
                      <tr className="text-left">
                        <th className="px-4 py-3 text-xs font-medium uppercase tracking-[0.08em] text-app-soft">
                          Reserva
                        </th>
                        <th className="px-4 py-3 text-xs font-medium uppercase tracking-[0.08em] text-app-soft">
                          Sala
                        </th>
                        <th className="px-4 py-3 text-xs font-medium uppercase tracking-[0.08em] text-app-soft">
                          Início
                        </th>
                        <th className="px-4 py-3 text-xs font-medium uppercase tracking-[0.08em] text-app-soft">
                          Status
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {visibleBookings.map((booking) => (
                        <tr className="border-t border-app-border" key={booking.id}>
                          <td className="px-4 py-3 text-sm font-medium text-app-strong">
                            {booking.title}
                          </td>
                          <td className="px-4 py-3 text-sm text-app-text">
                            {roomNameById.get(booking.room_id) ??
                              `Sala #${booking.room_id}`}
                          </td>
                          <td className="px-4 py-3 text-sm text-app-text">
                            {formatShortDateTime(booking.start_at)}
                          </td>
                          <td className="px-4 py-3">
                            <span
                              className={cn(
                                'inline-flex rounded-full px-2.5 py-1 text-xs font-medium',
                                booking.status === 'ACTIVE'
                                  ? 'bg-emerald-100 text-emerald-700'
                                  : 'bg-red-100 text-red-700',
                              )}
                            >
                              {booking.status === 'ACTIVE' ? 'Ativa' : 'Cancelada'}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="px-4 py-6 text-center text-sm text-app-text">
                  Nenhuma reserva encontrada.
                </div>
              )}
            </section>
          </>
        ) : null}
      </section>
    </section>
  )
}
