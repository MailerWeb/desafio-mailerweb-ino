import { createContext } from 'react'

export type ToastType = 'success' | 'error'

export type ShowToastInput = {
  type: ToastType
  message: string
  title?: string
  durationMs?: number
}

export type ToastContextValue = {
  showToast: (input: ShowToastInput) => void
  dismissToast: () => void
}

export const ToastContext = createContext<ToastContextValue | undefined>(
  undefined,
)
