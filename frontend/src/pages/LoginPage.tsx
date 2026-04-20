import { useState, type FormEvent } from 'react'
import { Navigate, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../features/auth/useAuth'
import { useToast } from '../features/feedback/useToast'

type LocationState = {
  from?: {
    pathname?: string
  }
}

export function LoginPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { isAuthenticated, login } = useAuth()
  const { showToast } = useToast()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const redirectTo =
    (location.state as LocationState | null)?.from?.pathname || '/'

  if (isAuthenticated) {
    return <Navigate to={redirectTo} replace />
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsSubmitting(true)

    try {
      await login({
        email: email.trim(),
        password,
      })
      navigate(redirectTo, { replace: true })
    } catch (submitError) {
      showToast({
        type: 'error',
        message:
          submitError instanceof Error
            ? submitError.message
            : 'Não foi possível entrar.',
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center px-4 py-6">
      <section className="w-full max-w-md rounded-panel border border-app-border bg-white/90 p-6 shadow-soft md:p-8">
        <span className="inline-flex rounded-full bg-app-muted px-3 py-1 text-xs font-medium text-app-strong">
          Meeting Room Booking
        </span>
        <h1 className="mt-4 text-3xl font-semibold tracking-tight text-app-strong">
          Acesse sua conta
        </h1>
        <p className="mt-2 text-sm leading-6 text-app-text">
          Entre com seu usuário para gerenciar salas, reservas e notificações.
        </p>

        <form className="mt-6 grid gap-4" onSubmit={handleSubmit}>
          <label className="grid gap-2">
            <span className="text-sm font-medium text-app-strong">E-mail</span>
            <input
              className="min-h-12 rounded-2xl border border-app-border bg-app-surface px-4 text-app-strong outline-none transition focus:border-app-strong"
              type="email"
              name="email"
              autoComplete="email"
              placeholder="voce@empresa.com"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
            />
          </label>

          <label className="grid gap-2">
            <span className="text-sm font-medium text-app-strong">Senha</span>
            <input
              className="min-h-12 rounded-2xl border border-app-border bg-app-surface px-4 text-app-strong outline-none transition focus:border-app-strong"
              type="password"
              name="password"
              autoComplete="current-password"
              placeholder="Sua senha"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
            />
          </label>

          <button
            className="inline-flex min-h-12 items-center justify-center rounded-2xl bg-app-strong px-4 text-sm font-medium text-white transition hover:bg-black disabled:cursor-not-allowed disabled:opacity-65"
            type="submit"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Entrando...' : 'Entrar'}
          </button>
        </form>
      </section>
    </main>
  )
}
