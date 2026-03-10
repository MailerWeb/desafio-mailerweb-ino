import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { bookingService, roomService } from '../services/auth'
import Alert from '../components/Alert'
import { formatDateInput, getDateFromInput } from '../utils/formatters'

export default function CreateBooking() {
  const [rooms, setRooms] = useState([])
  const [formData, setFormData] = useState({
    title: '',
    room_id: '',
    start_at: '',
    end_at: '',
    participants: '',
  })
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [alert, setAlert] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    fetchRooms()
  }, [])

  const fetchRooms = async () => {
    try {
      const data = await roomService.listRooms()
      setRooms(Array.isArray(data) ? data : [])
    } catch (error) {
      const message = error.response?.data?.detail || 'Erro ao carregar salas'
      setAlert({ type: 'error', message })
    } finally {
      setLoading(false)
    }
  }

  const validateForm = () => {
    if (!formData.title.trim()) {
      setAlert({ type: 'error', message: 'Título é obrigatório' })
      return false
    }

    if (!formData.room_id) {
      setAlert({ type: 'error', message: 'Sala é obrigatória' })
      return false
    }

    if (!formData.start_at) {
      setAlert({ type: 'error', message: 'Data/hora de início é obrigatória' })
      return false
    }

    if (!formData.end_at) {
      setAlert({ type: 'error', message: 'Data/hora de término é obrigatória' })
      return false
    }

    const start = new Date(formData.start_at)
    const end = new Date(formData.end_at)

    if (start >= end) {
      setAlert({
        type: 'error',
        message: 'A data/hora de término deve ser posterior à de início',
      })
      return false
    }

    const durationMinutes = (end - start) / 60000
    if (durationMinutes < 15) {
      setAlert({ type: 'error', message: 'Duração mínima é 15 minutos' })
      return false
    }

    if (durationMinutes > 480) {
      setAlert({ type: 'error', message: 'Duração máxima é 8 horas' })
      return false
    }

    return true
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!validateForm()) return

    setSubmitting(true)

    try {
      const participants = formData.participants
        .split(',')
        .map((p) => p.trim())
        .filter((p) => p)

      await bookingService.createBooking(
        formData.title,
        formData.room_id,
        getDateFromInput(formData.start_at),
        getDateFromInput(formData.end_at),
        participants
      )

      setAlert({
        type: 'success',
        message: 'Reserva criada com sucesso! Ainda processando notificações...',
      })
      setTimeout(() => navigate('/bookings'), 2000)
    } catch (error) {
      const message = error.response?.data?.detail || 'Erro ao criar reserva'
      setAlert({ type: 'error', message })
    } finally {
      setSubmitting(false)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

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
        <h1 style={{ color: 'white', marginBottom: '20px' }}>Criar Nova Reserva ✏️</h1>

        {alert && (
          <Alert
            type={alert.type}
            message={alert.message}
            onClose={() => setAlert(null)}
            autoClose={alert.type === 'success' ? 3000 : false}
          />
        )}

        <div className="card">
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="title">Título da Reunião</label>
              <input
                type="text"
                id="title"
                name="title"
                value={formData.title}
                onChange={handleChange}
                required
                placeholder="Ex: Reunião de Planejamento"
              />
            </div>

            <div className="form-group">
              <label htmlFor="room_id">Sala</label>
              <select
                id="room_id"
                name="room_id"
                value={formData.room_id}
                onChange={handleChange}
                required
              >
                <option value="">Selecionar sala...</option>
                {rooms.map((room) => (
                  <option key={room.id} value={room.id}>
                    {room.name} (Capacidade: {room.capacity})
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="start_at">Início</label>
              <input
                type="datetime-local"
                id="start_at"
                name="start_at"
                value={formData.start_at}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="end_at">Término</label>
              <input
                type="datetime-local"
                id="end_at"
                name="end_at"
                value={formData.end_at}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="participants">
                Participantes (emails separados por vírgula)
              </label>
              <textarea
                id="participants"
                name="participants"
                value={formData.participants}
                onChange={handleChange}
                placeholder="usuario1@example.com, usuario2@example.com"
                rows="4"
                style={{ fontFamily: 'monospace' }}
              />
            </div>

            <div
              style={{
                display: 'flex',
                gap: '10px',
                marginTop: '20px',
              }}
            >
              <button type="submit" className="btn btn-primary" disabled={submitting}>
                {submitting ? 'Criando...' : 'Criar Reserva'}
              </button>
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => navigate('/bookings')}
              >
                Cancelar
              </button>
            </div>
          </form>

          <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f0f7ff', borderRadius: '5px' }}>
            <p style={{ fontSize: '14px', color: '#333' }}>
              <strong>ℹ️ Informações:</strong>
              <br />
              • Duração mínima: 15 minutos
              <br />
              • Duração máxima: 8 horas
              <br />
              • Os participantes receberão notificação por email
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
