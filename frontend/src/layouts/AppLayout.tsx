import { NavLink, Outlet } from 'react-router-dom'
import { useAuth } from '../features/auth/useAuth'

export function AppLayout() {
  const { user, logout } = useAuth()

  function getNavClassName(isActive: boolean) {
    return [
      'inline-flex min-h-10 items-center justify-center rounded-full px-4 text-sm font-medium transition-colors',
      isActive
        ? 'bg-app-strong text-app-surface shadow-sm'
        : 'text-app-text hover:bg-white/80 hover:text-app-strong',
    ].join(' ')
  }

  return (
    <main className="min-h-screen bg-transparent px-4 py-4 md:px-8 md:py-8">
      <header className="mx-auto flex w-full max-w-6xl flex-col gap-4 rounded-panel border border-app-border bg-white/90 p-4 shadow-soft backdrop-blur md:flex-row md:items-center md:justify-between md:gap-6">
        <div className="flex min-w-0 items-center gap-3">

          <div className="min-w-0">
            <p className="truncate text-sm font-semibold text-app-strong">
              Meeting Room Booking
            </p>
            <p className="truncate text-xs text-app-soft">Gestão de salas</p>
          </div>
        </div>

        <nav
          className="flex items-center gap-2 overflow-x-auto rounded-full border border-app-border bg-app-muted/80 p-1"
          aria-label="Navegação principal"
        >
          <NavLink
            to="/"
            end
            className={({ isActive }) => getNavClassName(isActive)}
          >
            Visão geral
          </NavLink>
          <NavLink
            to="/rooms"
            className={({ isActive }) => getNavClassName(isActive)}
          >
            Salas
          </NavLink>
          <NavLink
            to="/bookings"
            className={({ isActive }) => getNavClassName(isActive)}
          >
            Reservas
          </NavLink>
        </nav>

        <div className="flex items-center justify-between gap-3 md:justify-end">
          <div className="min-w-0 text-right">
            <p className="truncate text-sm font-semibold text-app-strong">
              {user?.full_name}
            </p>
            <p className="truncate text-xs text-app-soft">{user?.email}</p>
          </div>
          <button
            className="inline-flex min-h-10 items-center justify-center rounded-xl border border-app-border px-4 text-sm font-medium text-app-strong transition-colors hover:bg-app-muted"
            type="button"
            onClick={logout}
          >
            Sair
          </button>
        </div>
      </header>

      <section className="mx-auto mt-4 w-full max-w-6xl">
        <Outlet />
      </section>
    </main>
  )
}
