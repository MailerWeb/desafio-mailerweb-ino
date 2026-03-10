import { useState, useEffect } from 'react'
import { roomService } from '../services/auth'
import Alert from '../components/Alert'

export default function Rooms() {
  const [rooms, setRooms] = useState([])
  const [loading, setLoading] = useState(true)
  const [alert, setAlert] = useState(null)
  const [newRoom, setNewRoom] = useState({ name: '', capacity: '' })
  const [showForm, setShowForm] = useState(false)
  const [formLoading, setFormLoading] = useState(false)

  useEffect(() => {
    fetchRooms()
  }, [])

  const fetchRooms = async () => {
    setLoading(true)
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

  const handleCreateRoom = async (e) => {
    e.preventDefault()
    setFormLoading(true)

    try {
      await roomService.createRoom(newRoom.name, parseInt(newRoom.capacity))
      setAlert({
        type: 'success',
        message: 'Sala criada com sucesso!',
      })
      setNewRoom({ name: '', capacity: '' })
      setShowForm(false)
      await fetchRooms()
    } catch (error) {
      const message = error.response?.data?.detail || 'Erro ao criar sala'
      setAlert({ type: 'error', message })
    } finally {
      setFormLoading(false)
    }
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
        <h1 style={{ color: 'white', marginBottom: '20px' }}>Salas 🏢</h1>

        {alert && (
          <Alert
            type={alert.type}
            message={alert.message}
            onClose={() => setAlert(null)}
          />
        )}

        <button
          className="btn btn-primary"
          onClick={() => setShowForm(!showForm)}
          style={{ marginBottom: '20px' }}
        >
          {showForm ? 'Cancelar' : '+ Nova Sala'}
        </button>

        {showForm && (
          <div className="card">
            <h2>Criar Nova Sala</h2>
            <form onSubmit={handleCreateRoom} style={{ marginTop: '20px' }}>
              <div className="form-group">
                <label htmlFor="name">Nome da Sala</label>
                <input
                  type="text"
                  id="name"
                  value={newRoom.name}
                  onChange={(e) => setNewRoom({ ...newRoom, name: e.target.value })}
                  required
                  placeholder="Ex: Sala de Reunições A"
                />
              </div>

              <div className="form-group">
                <label htmlFor="capacity">Capacidade</label>
                <input
                  type="number"
                  id="capacity"
                  value={newRoom.capacity}
                  onChange={(e) => setNewRoom({ ...newRoom, capacity: e.target.value })}
                  required
                  min="1"
                  placeholder="Ex: 10"
                />
              </div>

              <button type="submit" className="btn btn-primary" disabled={formLoading}>
                {formLoading ? 'Criando...' : 'Criar Sala'}
              </button>
            </form>
          </div>
        )}

        {rooms.length === 0 ? (
          <div className="empty-state">
            <h2>Nenhuma sala disponível</h2>
            <p>Crie a primeira sala para começar!</p>
          </div>
        ) : (
          <div className="grid">
            {rooms.map((room) => (
              <div key={room.id} className="room-card">
                <h3>📍 {room.name}</h3>
                <p>
                  <strong>Capacidade:</strong> {room.capacity} pessoas
                </p>
                <p className="text-muted">ID: {room.id}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
