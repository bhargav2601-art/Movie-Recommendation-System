import { MotionConfig, motion } from 'framer-motion'
import { Clock3, Languages, PlayCircle, Star, Ticket } from 'lucide-react'
import { useState } from 'react'
import { Link } from 'react-router-dom'

import { currency, moviePaletteStyle } from '../../lib/utils'
import { TrailerModal } from '../common/TrailerModal'
import { Button } from '../ui/button'
import { Card } from '../ui/card'

export function MovieCard({ movie, compact = false }) {
  const [showTrailer, setShowTrailer] = useState(false)
  const cardWidthClass = compact ? 'min-h-[29rem]' : 'min-h-[32rem]'

  return (
    <>
      <MotionConfig transition={{ duration: 0.28 }}>
        <motion.div whileHover={{ y: -6 }} className="h-full">
          <Card
            className="group flex h-full flex-col overflow-hidden border-border/25 bg-card-strong/90"
            style={moviePaletteStyle(movie)}
          >
            <div className={`relative aspect-[2/3] overflow-hidden ${cardWidthClass}`}>
              <img
                src={movie.poster}
                alt={movie.title}
                className="absolute inset-0 h-full w-full object-cover object-center transition duration-500 group-hover:scale-[1.03]"
              />
              <img
                src={movie.backdrop}
                alt=""
                aria-hidden="true"
                className="absolute inset-0 h-full w-full object-cover object-center opacity-0 transition duration-500 group-hover:opacity-35"
              />
              <div className="absolute inset-0 bg-[linear-gradient(180deg,rgba(3,6,16,0.02),rgba(3,6,16,0.18)_36%,rgba(3,6,16,0.95)_100%)]" />

              <div className="absolute left-4 right-4 top-4 flex items-start justify-between gap-3">
                <span className="inline-flex max-w-[75%] items-center rounded-full border border-white/15 bg-black/30 px-3 py-2 text-[11px] uppercase tracking-[0.28em] text-white backdrop-blur-xl">
                  <span className="truncate">{movie.trendingBadge}</span>
                </span>
                <span className="rounded-full border border-white/15 bg-black/30 px-3 py-2 text-xs font-semibold text-white/90 backdrop-blur-xl">
                  {movie.certificate}
                </span>
              </div>

              <div className="absolute inset-x-0 bottom-0 p-4">
                {movie.logo ? (
                  <img
                    src={movie.logo}
                    alt={`${movie.title} logo`}
                    className="mb-3 h-14 max-w-[80%] object-contain object-left brightness-125"
                  />
                ) : (
                  <h3 className="mb-3 max-w-[85%] text-balance font-display text-2xl font-extrabold text-white">
                    {movie.title}
                  </h3>
                )}

                <div className="flex flex-wrap items-center gap-3 text-xs text-white/78">
                  <span className="inline-flex items-center gap-1.5">
                    <Star className="size-3.5 fill-gold text-gold" />
                    {movie.imdbScore.toFixed(1)}
                  </span>
                  <span className="inline-flex items-center gap-1.5">
                    <Clock3 className="size-3.5" />
                    {movie.duration}
                  </span>
                  <span className="inline-flex items-center gap-1.5">
                    <Languages className="size-3.5" />
                    {movie.language?.[0]}
                  </span>
                </div>
              </div>

              <button
                type="button"
                onClick={() => setShowTrailer(true)}
                className="absolute right-4 top-1/2 inline-flex -translate-y-1/2 items-center gap-2 rounded-full border border-white/20 bg-black/45 px-4 py-2 text-sm font-semibold text-white opacity-0 shadow-lg backdrop-blur-xl transition duration-300 group-hover:opacity-100"
              >
                <PlayCircle className="size-4" style={{ color: 'var(--movie-accent)' }} />
                Trailer
              </button>
            </div>

            <div className="flex flex-1 flex-col justify-between gap-5 px-4 py-4">
              <div className="space-y-4">
                <div className="flex flex-wrap gap-2">
                  {movie.genre.slice(0, 3).map((item) => (
                    <span
                      key={item}
                      className="rounded-full border border-border/25 bg-card/55 px-3 py-1 text-xs text-muted backdrop-blur-md"
                    >
                      {item}
                    </span>
                  ))}
                </div>
                <p className="line-clamp-2 min-h-[3rem] text-sm leading-6 text-muted">{movie.heroTag || movie.storyline}</p>
              </div>

              <div className="flex items-end justify-between gap-4">
                <div>
                  <p className="text-xs uppercase tracking-[0.28em] text-subtle">From</p>
                  <p className="mt-1 font-semibold text-foreground">{currency(movie.shows?.[0]?.pricing?.base || 220)}</p>
                </div>
                <div className="flex shrink-0 gap-2">
                  <Button variant="secondary" size="sm" onClick={() => setShowTrailer(true)}>
                    <PlayCircle className="mr-2 size-4" />
                    Watch
                  </Button>
                  <Link to={movie.shows?.[0]?.id ? `/booking/${movie.shows[0].id}` : `/movies/${movie.id}`}>
                    <Button size="sm">
                      <Ticket className="mr-2 size-4" />
                      {movie.shows?.[0]?.id ? 'Book' : 'Details'}
                    </Button>
                  </Link>
                </div>
              </div>
            </div>
          </Card>
        </motion.div>
      </MotionConfig>

      <TrailerModal movie={movie} open={showTrailer} onClose={() => setShowTrailer(false)} />
    </>
  )
}
