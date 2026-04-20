import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type PropsWithChildren,
} from 'react'
import {
  ToastContext,
  type ShowToastInput,
  type ToastContextValue,
  type ToastType,
} from './context'

type ToastState = ShowToastInput & {
  id: number
}

const DEFAULT_DURATION_BY_TYPE: Record<ToastType, number> = {
  success: 3200,
  error: 4200,
}

const EXIT_ANIMATION_MS = 180

function getToastStyle(type: ToastType) {
  if (type === 'error') {
    return {
      container:
        'border-red-200 bg-red-50 text-red-700 shadow-red-100/80',
      badge: 'bg-red-100 text-red-700',
      button:
        'text-red-500 hover:bg-red-100 hover:text-red-700 focus-visible:ring-red-200',
    }
  }

  return {
    container:
      'border-emerald-200 bg-emerald-50 text-emerald-700 shadow-emerald-100/80',
    badge: 'bg-emerald-100 text-emerald-700',
    button:
      'text-emerald-500 hover:bg-emerald-100 hover:text-emerald-700 focus-visible:ring-emerald-200',
  }
}

function ToastViewport({
  toast,
  isVisible,
  onDismiss,
}: {
  toast: ToastState
  isVisible: boolean
  onDismiss: () => void
}) {
  const style = getToastStyle(toast.type)

  return (
    <div className="pointer-events-none fixed inset-x-4 top-4 z-50 flex justify-center md:inset-x-auto md:right-6 md:top-6 md:justify-end">
      <div
        className={[
          'pointer-events-auto w-full max-w-sm rounded-3xl border px-4 py-4 shadow-lg backdrop-blur transition-all duration-200 ease-out',
          style.container,
          isVisible
            ? 'translate-y-0 opacity-100 md:translate-x-0'
            : '-translate-y-2 opacity-0 md:translate-x-3 md:translate-y-0',
        ].join(' ')}
        role={toast.type === 'error' ? 'alert' : 'status'}
        aria-live={toast.type === 'error' ? 'assertive' : 'polite'}
      >
        <div className="flex items-start gap-3">
          <span
            className={[
              'inline-flex min-h-8 min-w-8 items-center justify-center rounded-full px-2 text-[11px] font-semibold uppercase tracking-[0.14em]',
              style.badge,
            ].join(' ')}
          >
            {toast.type === 'error' ? 'Erro' : 'Ok'}
          </span>

          <div className="min-w-0 flex-1">
            {toast.title ? (
              <p className="text-sm font-semibold text-slate-950">{toast.title}</p>
            ) : null}
            <p className="text-sm leading-6">{toast.message}</p>
          </div>

          <button
            className={[
              'inline-flex min-h-8 min-w-8 items-center justify-center rounded-full text-sm font-medium transition focus-visible:outline-none focus-visible:ring-2',
              style.button,
            ].join(' ')}
            type="button"
            aria-label="Fechar"
            onClick={onDismiss}
          >
            ×
          </button>
        </div>
      </div>
    </div>
  )
}

export function ToastProvider({ children }: PropsWithChildren) {
  const [toast, setToast] = useState<ToastState | null>(null)
  const [isVisible, setIsVisible] = useState(false)
  const nextIdRef = useRef(0)
  const dismissTimeoutRef = useRef<number | null>(null)
  const clearTimeoutRef = useRef<number | null>(null)

  const clearTimers = useCallback(() => {
    if (dismissTimeoutRef.current !== null) {
      window.clearTimeout(dismissTimeoutRef.current)
      dismissTimeoutRef.current = null
    }

    if (clearTimeoutRef.current !== null) {
      window.clearTimeout(clearTimeoutRef.current)
      clearTimeoutRef.current = null
    }
  }, [])

  const dismissToast = useCallback(() => {
    clearTimers()
    setIsVisible(false)
    clearTimeoutRef.current = window.setTimeout(() => {
      setToast(null)
      clearTimeoutRef.current = null
    }, EXIT_ANIMATION_MS)
  }, [clearTimers])

  const showToast = useCallback(
    (input: ShowToastInput) => {
      clearTimers()
      nextIdRef.current += 1
      setToast({
        id: nextIdRef.current,
        ...input,
      })
      setIsVisible(true)
    },
    [clearTimers],
  )

  useEffect(() => {
    if (!toast) {
      return
    }

    dismissTimeoutRef.current = window.setTimeout(() => {
      dismissToast()
    }, toast.durationMs ?? DEFAULT_DURATION_BY_TYPE[toast.type])

    return () => {
      if (dismissTimeoutRef.current !== null) {
        window.clearTimeout(dismissTimeoutRef.current)
        dismissTimeoutRef.current = null
      }
    }
  }, [dismissToast, toast])

  useEffect(() => () => clearTimers(), [clearTimers])

  const value = useMemo<ToastContextValue>(
    () => ({
      showToast,
      dismissToast,
    }),
    [dismissToast, showToast],
  )

  return (
    <ToastContext.Provider value={value}>
      {children}
      {toast ? (
        <ToastViewport
          toast={toast}
          isVisible={isVisible}
          onDismiss={dismissToast}
        />
      ) : null}
    </ToastContext.Provider>
  )
}
