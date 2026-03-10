export const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('pt-BR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export const formatTime = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleTimeString('pt-BR', {
    hour: '2-digit',
    minute: '2-digit',
  })
}

export const formatDateInput = (dateString) => {
  const date = new Date(dateString)
  return date.toISOString().slice(0, 16)
}

export const getDateFromInput = (inputValue) => {
  return new Date(inputValue).toISOString()
}

export const calculateDuration = (startAt, endAt) => {
  const start = new Date(startAt)
  const end = new Date(endAt)
  const minutes = (end - start) / 60000
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`
}
