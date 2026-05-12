import { motion } from 'framer-motion'
import { Moon, Sun } from 'lucide-react'

import { useTheme } from '../../context/ThemeProvider'

export function ThemeToggle() {
  const { resolvedTheme, toggleTheme } = useTheme()
  const isDark = resolvedTheme === 'dark'

  return (
    <button
      type="button"
      onClick={toggleTheme}
      className="group relative inline-flex h-12 w-24 items-center rounded-full border border-border/60 bg-card/80 p-1 shadow-card backdrop-blur-2xl transition-all duration-500 hover:scale-[1.03] hover:shadow-glow"
      aria-label={`Switch to ${isDark ? 'light' : 'dark'} mode`}
    >
      <span className="sr-only">{`Switch to ${isDark ? 'light' : 'dark'} mode`}</span>
      <span className="pointer-events-none absolute inset-0 rounded-full bg-[radial-gradient(circle_at_top,rgba(var(--accent-rgb),0.18),transparent_58%)] opacity-0 transition-opacity duration-500 group-hover:opacity-100" />
      <motion.span
        layout
        transition={{ type: 'spring', stiffness: 420, damping: 28 }}
        className={`absolute top-1 flex h-10 w-10 items-center justify-center rounded-full border border-border/50 ${
          isDark
            ? 'left-1 bg-[linear-gradient(135deg,rgba(var(--gold-rgb),0.92),rgba(var(--accent-rgb),0.92))] text-[rgb(var(--background-deep-rgb))]'
            : 'left-[calc(100%-2.75rem)] bg-[linear-gradient(135deg,rgba(255,255,255,0.95),rgba(var(--background-rgb),0.94))] text-gold'
        } shadow-[0_0_24px_rgba(var(--accent-rgb),0.28)]`}
      >
        <motion.span
          key={resolvedTheme}
          initial={{ rotate: -90, opacity: 0, scale: 0.6 }}
          animate={{ rotate: 0, opacity: 1, scale: 1 }}
          exit={{ rotate: 90, opacity: 0, scale: 0.6 }}
          transition={{ duration: 0.35 }}
        >
          {isDark ? <Moon className="size-4" /> : <Sun className="size-4" />}
        </motion.span>
      </motion.span>
      <span className="relative z-10 flex w-full items-center justify-between px-3 text-subtle">
        <Sun className={`size-4 transition-all duration-500 ${isDark ? 'opacity-45' : 'scale-110 text-gold'}`} />
        <Moon className={`size-4 transition-all duration-500 ${isDark ? 'scale-110 text-foreground' : 'opacity-45'}`} />
      </span>
      <span className="pointer-events-none absolute -bottom-11 left-1/2 -translate-x-1/2 rounded-full border border-border/60 bg-card/95 px-3 py-1 text-[11px] font-medium text-muted opacity-0 shadow-card backdrop-blur-xl transition-all duration-300 group-hover:-translate-y-1 group-hover:opacity-100">
        {isDark ? 'Dark mode active' : 'Light mode active'}
      </span>
    </button>
  )
}
