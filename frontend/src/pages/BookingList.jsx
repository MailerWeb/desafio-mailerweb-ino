import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { bookingService } from '../services/auth'
import Alert from '../components/Alert'
import { formatDate, calculateDuration } from '../utils/formatters'

export default function BookingList() {
  const [bookings, setBookings] = useState([])
  const [loading, setLoading] = useState(true)
  const [alert, setAlert] = useState(null)
  const [filter, setFilter] = useState('all')
  const navigate = useNavigate()

  useEffect(() => {
    fetchBookings()
  }, [])

  const fetchBookings = async () => {
    setLoading(true)
    try {
      const data = await bookingService.listBookings()
      setBookings(Array.isArray(data) ? data : [])
    } catch (error) {
      const message = error.response?.data?.detail || 'Erro ao carregar reservas'
      setAlert({ type: 'error', message })
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    if (!window.confirm('Tem certeza que deseja cancelar esta reserva?')) return

    try {
      await bookingService.cancelBooking(id)
      setAlert({
        type: 'success',
        message: 'Reserva cancelada com sucesso!',
      })
      await fetchBookings()
    } catch (error) {
      const message = error.response?.data?.detail || 'Erro ao cancelar reserva'
      setAlert({ type: 'error', message })
    }
  }

  const getFilteredBookings = () => {
    if (filter === 'active') {
      return bookings.filter((b) => b.status === 'active')
    }
    if (filter === 'cancelled') {
      return bookings.filter((b) => b.status === 'cancelled')
    }
    return bookings
  }

  const filteredBookings = getFilteredBookings()

  if (loading) {
    return (
      <div className="container">
        <div className="loading-container">
          <div className="spinner"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="container">
      <div style={{ marginTop: '20px' }}>
        <h1 style={{ color: 'white', marginBottom: '20px' }}>Minhas Reservas 📅</h1>

        {alert && (
          <Alert
            type={alert.type}
            message={alert.message}
            onClose={() => setAlert(null)}
          />
        )}

        <div style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
          <button
            className={`btn ${filter === 'all' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setFilter('all')}
          >
            Todas ({bookings.length})
          </button>
          <button
            className={`btn ${filter === 'active' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setFilter('active')}
          >
            Ativas ({bookings.filter((b) => b.status === 'active').length})
          </button>
          <button
            className={`btn ${filter === 'cancelled' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setFilter('cancelled')}
          >
            Canceladas ({bookings.filter((b) => b.status === 'cancelled').length})
          </button>
        </div>

        <button
          className="btn btn-primary"
          onClick={() => navigate('/bookings/new')}
          style={{ marginBottom: '20px' }}
        >
          + Nova Reserva
        </button>

        {filteredBookings.length === 0 ? (
          <div className="empty-state">
            <h2>Nenhuma reserva encontrada</h2>
            <p>Crie uma nova reserva para começar!</p>
            <button
              className="btn btn-primary"
              onClick={() => navigate('/bookings/new')}
            >
              Criar Reserva
            </button>
          </div>
        ) : (
          <div className="grid">
            {filteredBookings.map((booking) => (
              <div
                key={booking.id}
                className="booking-card"
                style={{
                  opacity: booking.status === 'cancelled' ? 0.7 : 1,
                  textDecoration: booking.status === 'cancelled' ? 'line-through' : 'none',
                }}
              >
                <h3>{booking.title}</h3>
                <p>
                  <strong>Sala:</strong> {booking.room_id}
                </p>
                <p>
                  <strong>Início:</strong> {formatDate(booking.start_at)}
                </p>
                <p>
                  <strong>Término:</strong> {formatDate(booking.end_at)}
                </p>
                <p>
                  <strong>Duração:</strong> {calculateDuration(booking.start_at, booking.end_at)}
                </p>
                <p>
                  <strong>Participantes:</strong> {booking.participants?.length || 0}
                </p>
                <p>
                  <strong>Status:</strong>{' '}
                  <span
                    style={{
                      padding: '4px 8px',
                      borderRadius: '3px',
                      fontSize: '12px',
                      backgroundColor:
                        booking.status === 'active' ? '#d4edda' : '#f8d7da',
                      color: booking.status === 'active' ? '#155724' : '#721c24',
                    }}
                  >
                    {booking.status === 'active' ? 'Ativa' : 'Cancelada'}
                  </span>
                </p>

                {booking.status === 'active' && (
                  <div className="actions-button">
                    <button
                      className="btn btn-secondary btn-small"
                      onClick={() => navigate(`/bookings/${booking.id}/edit`)}
                    >
                      ✏️ Editar
                    </button>
                    <button
                      className="btn btn-danger btn-small"
                      onClick={() => handleDelete(booking.id)}
                    >
                      🗑️ Cancelar
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
