import { render, type RenderOptions } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import type { PropsWithChildren, ReactElement } from 'react'
import { ToastProvider } from '../features/feedback/ToastProvider'

type Options = RenderOptions & {
  route?: string
}

export function renderWithRouter(
  ui: ReactElement,
  { route = '/', ...options }: Options = {},
) {
  function Wrapper({ children }: PropsWithChildren) {
    return (
      <MemoryRouter initialEntries={[route]}>
        <ToastProvider>{children}</ToastProvider>
      </MemoryRouter>
    )
  }

  return render(ui, {
    wrapper: Wrapper,
    ...options,
  })
}
