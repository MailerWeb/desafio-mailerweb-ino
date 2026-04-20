import { act, fireEvent, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi, afterEach } from 'vitest'
import { useToast } from './useToast'
import { renderWithRouter } from '../../test/renderWithRouter'

function ToastHarness() {
  const { dismissToast, showToast } = useToast()

  return (
    <div className="flex gap-2">
      <button
        type="button"
        onClick={() =>
          showToast({
            type: 'success',
            message: 'Toast de sucesso',
            durationMs: 600,
          })
        }
      >
        Mostrar sucesso
      </button>
      <button
        type="button"
        onClick={() =>
          showToast({
            type: 'error',
            message: 'Toast de erro',
            durationMs: 600,
          })
        }
      >
        Mostrar erro
      </button>
      <button
        type="button"
        onClick={() =>
          showToast({
            type: 'success',
            message: 'Toast substituto',
            durationMs: 600,
          })
        }
      >
        Substituir
      </button>
      <button type="button" onClick={dismissToast}>
        Fechar por API
      </button>
    </div>
  )
}

describe('ToastProvider', () => {
  afterEach(() => {
    vi.useRealTimers()
  })

  it('substitui o toast anterior por um novo', async () => {
    const user = userEvent.setup()

    renderWithRouter(<ToastHarness />)

    await user.click(screen.getByRole('button', { name: /mostrar sucesso/i }))
    await screen.findByText('Toast de sucesso')

    await user.click(screen.getByRole('button', { name: /substituir/i }))

    expect(screen.queryByText('Toast de sucesso')).not.toBeInTheDocument()
    expect(screen.getByText('Toast substituto')).toBeInTheDocument()
  })

  it('fecha o toast pelo botão do usuário', () => {
    vi.useFakeTimers()

    renderWithRouter(<ToastHarness />)

    fireEvent.click(screen.getByRole('button', { name: /mostrar erro/i }))
    expect(screen.getByText('Toast de erro')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: /^fechar$/i }))

    act(() => {
      vi.advanceTimersByTime(200)
    })

    expect(screen.queryByText('Toast de erro')).not.toBeInTheDocument()
  })

  it('fecha o toast automaticamente após o timeout', () => {
    vi.useFakeTimers()

    renderWithRouter(<ToastHarness />)

    fireEvent.click(screen.getByRole('button', { name: /mostrar sucesso/i }))
    expect(screen.getByText('Toast de sucesso')).toBeInTheDocument()

    act(() => {
      vi.advanceTimersByTime(1000)
    })

    expect(screen.queryByText('Toast de sucesso')).not.toBeInTheDocument()
  })
})
