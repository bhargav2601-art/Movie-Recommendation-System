import { cn } from '../../lib/utils'

export function Input({ className, ...props }) {
  return (
    <input
      className={cn(
        'w-full rounded-2xl border border-border/50 bg-background-elevated/75 px-4 py-3 text-sm text-foreground placeholder:text-subtle shadow-sm outline-none focus:border-neon/60 focus:ring-2 focus:ring-neon/20',
        className,
      )}
      {...props}
    />
  )
}
