import { ChevronLeft, ChevronRight } from 'lucide-react'
import { useState } from 'react'


export function MediaCarousel({ items = [], title }) {
  const [active, setActive] = useState(0)

  if (!items.length) return null

  const current = items[active]
  const move = (delta) => setActive((value) => (value + delta + items.length) % items.length)

  return (
    <div>
      <div className="relative overflow-hidden rounded-[30px] border border-border/30 bg-overlay/20">
        <img src={current} alt={title} className="aspect-video w-full object-cover" />
        <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-overlay/55 via-transparent to-overlay/10" />
        <div className="absolute inset-x-0 bottom-0 flex items-center justify-between p-4">
          <p className="text-sm uppercase tracking-[0.35em] text-foreground/70">Gallery</p>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => move(-1)}
              className="glass-button inline-flex size-10 items-center justify-center text-muted hover:text-foreground"
            >
              <ChevronLeft className="size-4" />
            </button>
            <button
              type="button"
              onClick={() => move(1)}
              className="glass-button inline-flex size-10 items-center justify-center text-muted hover:text-foreground"
            >
              <ChevronRight className="size-4" />
            </button>
          </div>
        </div>
      </div>

      <div className="mt-4 grid gap-3 md:grid-cols-3">
        {items.map((item, index) => (
          <button
            key={item}
            type="button"
            onClick={() => setActive(index)}
            className={`overflow-hidden rounded-[22px] border transition ${
              index === active ? 'border-gold/60' : 'border-border/30'
            }`}
          >
            <img src={item} alt={`${title} ${index + 1}`} className="aspect-video w-full object-cover" />
          </button>
        ))}
      </div>
    </div>
  )
}
