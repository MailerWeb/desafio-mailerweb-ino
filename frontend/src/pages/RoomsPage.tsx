import { useEffect, useState, type FormEvent } from 'react'
import axios from 'axios'
import { createRoom, fetchRooms } from '../features/rooms/roomsApi'
import type { Room } from '../features/rooms/types'

function getRoomsErrorMessage(error: unknown) {
  if (axios.isAxiosError(error)) {
    return (
      error.response?.data?.detail ??
      'Nao foi possivel carregar as salas no momento.'
    )
  }

  return 'Nao foi possivel carregar as salas no momento.'
}

function getCreateRoomErrorMessage(error: unknown) {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail

    if (detail === 'Room name already exists') {
      return 'Ja existe uma sala cadastrada com esse nome.'
    }

    if (typeof detail === 'string' && detail.trim()) {
      return detail
    }
  }

  return 'Nao foi possivel criar a sala no momento.'
}

function sortRoomsByName(items: Room[]) {
  return [...items].sort((firstRoom, secondRoom) =>
    firstRoom.name.localeCompare(secondRoom.name, 'pt-BR'),
  )
}

export function RoomsPage() {
  const [rooms, setRooms] = useState<Room[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [loadError, setLoadError] = useState('')
  const [createError, setCreateError] = useState('')
  const [successMessage, setSuccessMessage] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [name, setName] = useState('')
  const [capacity, setCapacity] = useState('8')

  useEffect(() => {
    let isMounted = true

    fetchRooms()
      .then((response) => {
        if (!isMounted) return
        setRooms(sortRoomsByName(response))
        setLoadError('')
      })
      .catch((requestError) => {
        if (!isMounted) return
        setLoadError(getRoomsErrorMessage(requestError))
      })
      .finally(() => {
        if (!isMounted) return
        setIsLoading(false)
      })

    return () => {
      isMounted = false
    }
  }, [])

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsSubmitting(true)
    setCreateError('')
    setSuccessMessage('')

    try {
      const createdRoom = await createRoom({
        name: name.trim(),
        capacity: Number(capacity),
      })

      setRooms((currentRooms) => sortRoomsByName([...currentRooms, createdRoom]))
      setName('')
      setCapacity('8')
      setSuccessMessage('Sala criada com sucesso.')
    } catch (submitError) {
      setCreateError(getCreateRoomErrorMessage(submitError))
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <section className="surface-card">
      <div className="section-header">
        <div>
          <div className="status-chip">Salas</div>
          <h2 className="section-title">Salas disponiveis</h2>
          <p className="section-copy">
            Cadastre novas salas e acompanhe quais ambientes ja estao
            disponiveis para as reservas.
          </p>
        </div>
      </div>

      <form className="room-form" onSubmit={handleSubmit}>
        <div className="form-grid">
          <label className="field">
            <span>Nome da sala</span>
            <input
              type="text"
              name="name"
              placeholder="Ex.: Sala Atlas"
              value={name}
              onChange={(event) => setName(event.target.value)}
              required
            />
          </label>

          <label className="field">
            <span>Capacidade</span>
            <input
              type="number"
              name="capacity"
              min={1}
              step={1}
              inputMode="numeric"
              value={capacity}
              onChange={(event) => setCapacity(event.target.value)}
              required
            />
          </label>
        </div>

        <div className="room-form__actions">
          <button
            className="primary-button primary-button--inline"
            type="submit"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Criando sala...' : 'Criar sala'}
          </button>
        </div>
      </form>

      {createError ? (
        <div className="feedback feedback--error" role="alert">
          {createError}
        </div>
      ) : null}

      {successMessage ? (
        <div className="feedback feedback--success" role="status">
          {successMessage}
        </div>
      ) : null}

      {isLoading ? (
        <div className="state-card" aria-live="polite">
          <strong>Carregando salas...</strong>
          <p>Estamos consultando a API protegida para montar a lista.</p>
        </div>
      ) : null}

      {!isLoading && loadError ? (
        <div className="feedback feedback--error" role="alert">
          {loadError}
        </div>
      ) : null}

      {!isLoading && !loadError && rooms.length === 0 ? (
        <div className="state-card">
          <strong>Nenhuma sala cadastrada</strong>
          <p>
            Crie a primeira sala por aqui para comecar a gerenciar reservas.
          </p>
        </div>
      ) : null}

      {!isLoading && !loadError && rooms.length > 0 ? (
        <div className="rooms-grid">
          {rooms.map((room) => (
            <article className="room-card" key={room.id}>
              <div className="room-card__header">
                <div>
                  <h3>{room.name}</h3>
                  <p>ID #{room.id}</p>
                </div>
                <span className="room-capacity">{room.capacity} lugares</span>
              </div>
            </article>
          ))}
        </div>
      ) : null}
    </section>
  )
}
