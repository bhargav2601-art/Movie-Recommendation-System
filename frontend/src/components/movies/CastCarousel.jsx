import { AnimatePresence, motion } from 'framer-motion'
import { ExternalLink, Star, X } from 'lucide-react'
import { useEffect, useState } from 'react'

import { Card } from '../ui/card'

function ActorModal({ actor, onClose }) {
  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [onClose])

  if (!actor) return null

  return (
    <div className="fixed inset-0 z-[90] bg-overlay/80 backdrop-blur-xl">
      <button className="absolute inset-0" onClick={onClose} aria-label="Close actor profile" />
      <div className="section-shell relative flex min-h-screen items-center justify-center py-10">
        <div className="glass-panel relative grid w-full max-w-4xl gap-6 overflow-hidden rounded-[34px] p-6 md:grid-cols-[0.42fr_1fr]">
          <button
            className="absolute right-5 top-5 rounded-full border border-border/30 bg-card/55 p-3 text-muted"
            onClick={onClose}
          >
            <X className="size-5" />
          </button>
          <img src={actor.image} alt={actor.name} className="h-full min-h-96 w-full rounded-[28px] object-cover" />
          <div>
            <p className="text-xs uppercase tracking-[0.35em] text-neon/70">Cast Profile</p>
            <h3 className="mt-3 font-display text-4xl font-extrabold text-foreground">{actor.name}</h3>
            <p className="mt-2 text-lg text-gold">{actor.role}</p>
            <div className="mt-5 flex items-center gap-2 text-sm text-muted">
              <Star className="size-4 fill-gold text-gold" />
              Popularity {actor.popularity}
            </div>
            <p className="mt-5 text-sm leading-8 text-muted">{actor.bio}</p>

            <div className="mt-6 grid gap-5 md:grid-cols-2">
              <div>
                <p className="text-xs uppercase tracking-[0.35em] text-subtle">Filmography</p>
                <div className="mt-3 flex flex-wrap gap-2">
                  {actor.filmography.map((movie) => (
                    <span key={movie} className="rounded-full border border-border/30 bg-card/55 px-3 py-2 text-sm text-muted">
                      {movie}
                    </span>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-xs uppercase tracking-[0.35em] text-subtle">Other Movies</p>
                <div className="mt-3 flex flex-wrap gap-2">
                  {actor.otherMovies.map((movie) => (
                    <span key={movie} className="rounded-full border border-border/30 bg-card/55 px-3 py-2 text-sm text-muted">
                      {movie}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <a
              href={actor.imdbLink}
              target="_blank"
              rel="noreferrer"
              className="mt-8 inline-flex items-center gap-2 rounded-full border border-border/30 bg-card/55 px-5 py-3 text-sm text-muted"
            >
              IMDb profile
              <ExternalLink className="size-4" />
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}

export function CastCarousel({ cast = [] }) {
  const [active, setActive] = useState(null)
  const [start, setStart] = useState(0)

  useEffect(() => {
    if (cast.length <= 3) return undefined
    const timer = window.setInterval(() => {
      setStart((value) => (value + 1) % cast.length)
    }, 3400)
    return () => window.clearInterval(timer)
  }, [cast.length])

  const visible = cast.length <= 3 ? cast : [...cast.slice(start), ...cast.slice(0, start)].slice(0, 3)

  return (
    <>
      <div className="grid gap-4 md:grid-cols-3">
        {visible.map((actor, index) => (
          <motion.button
            key={`${actor.name}-${index}`}
            whileHover={{ y: -6, scale: 1.01 }}
            className="group rounded-[28px] border border-border/30 bg-card/55 p-4 text-left"
            onClick={() => setActive(actor)}
          >
            <div className="relative mx-auto h-36 w-36 overflow-hidden rounded-full border border-neon/20 shadow-[0_0_40px_rgba(105,230,255,0.14)]">
              <img src={actor.image} alt={actor.name} loading="lazy" className="h-full w-full object-cover transition duration-500 group-hover:scale-110" />
            </div>
            <div className="mt-4">
              <p className="font-semibold text-foreground">{actor.name}</p>
              <p className="mt-1 text-sm text-gold">{actor.role}</p>
              <p className="mt-2 text-xs text-subtle">Popularity {actor.popularity}</p>
              <p className="mt-3 line-clamp-3 text-sm leading-7 text-muted">{actor.bio}</p>
            </div>
          </motion.button>
        ))}
      </div>

      <AnimatePresence>{active ? <ActorModal actor={active} onClose={() => setActive(null)} /> : null}</AnimatePresence>
    </>
  )
}
