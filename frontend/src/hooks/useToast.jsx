import { createContext, useContext, useMemo, useState } from 'react'
import { AnimatePresence, MotionConfig, motion } from 'framer-motion'
import { CheckCircle2, XCircle } from 'lucide-react'

const ToastContext = createContext(null)

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([])

  const push = ({ title, tone = 'success' }) => {
    const id = crypto.randomUUID()
    setToasts((prev) => [...prev, { id, title, tone }])
    window.setTimeout(() => {
      setToasts((prev) => prev.filter((toast) => toast.id !== id))
    }, 2800)
  }

  const value = useMemo(() => ({ push }), [])

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div className="fixed right-4 top-4 z-50 space-y-3">
        <MotionConfig transition={{ duration: 0.22 }}>
          <AnimatePresence>
            {toasts.map((toast) => (
              <motion.div
                key={toast.id}
                initial={{ opacity: 0, y: -12 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -12 }}
                className="glass-panel flex min-w-72 items-center gap-3 rounded-2xl px-4 py-3"
              >
                {toast.tone === 'success' ? (
                  <CheckCircle2 className="size-5 text-neon" />
                ) : (
                  <XCircle className="size-5 text-danger" />
                )}
                <p className="text-sm text-foreground">{toast.title}</p>
              </motion.div>
            ))}
          </AnimatePresence>
        </MotionConfig>
      </div>
    </ToastContext.Provider>
  )
}

export function useToast() {
  const context = useContext(ToastContext)
  if (!context) {
    throw new Error('useToast must be used within ToastProvider')
  }
  return context
}
