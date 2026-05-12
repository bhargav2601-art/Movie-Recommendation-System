import { cva } from 'class-variance-authority'

import { cn } from '../../lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-full font-semibold transition-all duration-500 focus:outline-none focus:ring-2 focus:ring-neon/40 disabled:cursor-not-allowed disabled:opacity-50',
  {
    variants: {
      variant: {
        primary:
          'bg-gradient-to-r from-gold via-[#f7d489] to-neon px-5 py-3 text-ink shadow-[0_14px_36px_rgba(var(--gold-rgb),0.18)] hover:scale-[1.02] hover:shadow-glow',
        secondary: 'border border-border/50 bg-card/70 px-5 py-3 text-foreground hover:bg-card/90',
        ghost: 'px-4 py-2 text-muted hover:bg-card/65 hover:text-foreground',
      },
      size: {
        default: 'text-sm',
        lg: 'px-6 py-3.5 text-base',
        icon: 'h-11 w-11',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'default',
    },
  },
)

export function Button({ className, variant, size, ...props }) {
  return <button className={cn(buttonVariants({ variant, size, className }))} {...props} />
}
