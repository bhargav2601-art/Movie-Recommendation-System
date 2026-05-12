import { AnimatePresence, MotionConfig, motion } from 'framer-motion'
import { CalendarDays, ChevronRight, Clock3, PlayCircle, Star, Ticket } from 'lucide-react'
import { Link } from 'react-router-dom'

import { moviePaletteStyle } from '../../lib/utils'
import { Button } from '../ui/button'

export function CinematicHero({
  movie,
  movies = [],
  activeIndex = 0,
  onSelectMovie,
  onWatchTrailer,
  detailHref,
  bookingHref,
  minHeight = '78vh',
  gridClassName = 'lg:grid-cols-[1.1fr_0.9fr]',
  progressLabel = 'Spotlight Progress',
}) {
  if (!movie) return null

  const heroBackdrop = movie.backdrop || movie.gallery?.[0] || movie.poster
  const canCycle = movies.length > 1 && typeof onSelectMovie === 'function'
  const progressTotal = Math.max(movies.length || 1, 1)
  const progressValue = ((activeIndex + 1) / progressTotal) * 100
  const heroShow = movie.shows?.[0]
  const metadataItems = [
    {
      key: 'imdb',
      icon: <Star className="size-4 fill-gold text-gold" />,
      label: `IMDb ${movie.imdbScore.toFixed(1)}`,
    },
    { key: 'rating', label: movie.rating },
    { key: 'language', label: movie.language?.[0] },
    { key: 'duration', label: movie.duration },
  ].filter((item) => item.label)

  return (
    <MotionConfig transition={{ duration: 0.5 }}>
      <section
        className="relative overflow-hidden"
        style={{
          ...moviePaletteStyle(movie),
          minHeight,
        }}
      >
        <img
          src={heroBackdrop}
          alt={movie.title}
          className="absolute inset-0 h-full w-full object-cover object-center opacity-45"
        />
        <div className="absolute inset-0 bg-[linear-gradient(90deg,rgba(3,6,16,0.94)_0%,rgba(3,6,16,0.72)_46%,rgba(3,6,16,0.82)_100%)]" />
        <div
          className="absolute inset-0"
          style={{
            background:
              'radial-gradient(circle at 14% 18%, color-mix(in srgb, var(--movie-accent) 15%, transparent), transparent 24%), radial-gradient(circle at 82% 18%, color-mix(in srgb, var(--movie-primary) 16%, transparent), transparent 28%)',
          }}
        />

        <div className={`section-shell relative z-10 grid gap-10 py-28 lg:items-center ${gridClassName}`}>
          <AnimatePresence mode="wait">
            <motion.div
              key={`${movie.id}-copy`}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              <div className="space-y-4">
                <p className="inline-flex w-fit items-center gap-2 rounded-full border border-white/15 bg-black/30 px-4 py-2 text-xs uppercase tracking-[0.35em] text-white/85 backdrop-blur-xl">
                  <span
                    className="inline-block size-2 rounded-full shadow-[0_0_18px_var(--movie-accent)]"
                    style={{ backgroundColor: 'var(--movie-accent)' }}
                  />
                  {movie.trendingBadge}
                </p>
                <h1 className="max-w-[12ch] text-balance font-display text-[clamp(3rem,5vw,5rem)] font-extrabold leading-[0.95] text-white">
                  {movie.title}
                </h1>
                <p className="max-w-[60ch] text-base leading-[1.8] text-white/82 md:text-lg">{movie.storyline}</p>
              </div>

              <div className="flex flex-wrap items-center gap-3 text-sm text-white/78">
                {metadataItems.map((item) => (
                  <span key={item.key} className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-2 backdrop-blur-md">
                    {item.icon}
                    {item.label}
                  </span>
                ))}
              </div>

              <div className="flex flex-wrap gap-3">
                {movie.genre?.slice(0, 4).map((tag) => (
                  <span key={tag} className="rounded-full border border-white/12 bg-white/8 px-4 py-2 text-sm font-medium text-white/82 backdrop-blur-md">
                    {tag}
                  </span>
                ))}
              </div>

              <div className="flex flex-wrap gap-4 pt-2">
                {heroShow ? (
                  <Link to={bookingHref || `/booking/${heroShow.id}`}>
                    <Button size="lg" className="min-h-[56px] min-w-[180px]">
                      <Ticket className="mr-2 size-4" />
                      Book Tickets
                    </Button>
                  </Link>
                ) : null}
                <Button size="lg" variant="secondary" onClick={onWatchTrailer} className="min-h-[56px] min-w-[180px]">
                  <PlayCircle className="mr-2 size-4" />
                  {movie.trailerCta || 'Watch Trailer'}
                </Button>
                {detailHref ? (
                  <Link to={detailHref}>
                    <Button size="lg" variant="secondary" className="min-h-[56px] min-w-[180px]">
                      Explore Details
                      <ChevronRight className="ml-2 size-4" />
                    </Button>
                  </Link>
                ) : null}
              </div>

              <div className="flex flex-wrap items-center gap-4 text-sm text-white/64">
                <span>Now booking in {movie.cities?.length ?? 0} cities</span>
                <span>•</span>
                <span>{movie.certificate}</span>
                {heroShow ? (
                  <>
                    <span>•</span>
                    <span className="inline-flex items-center gap-2">
                      <CalendarDays className="size-4" />
                      {heroShow.showDate} • {heroShow.showTime}
                    </span>
                  </>
                ) : null}
              </div>
            </motion.div>
          </AnimatePresence>

          <motion.div
            key={`${movie.id}-visual`}
            initial={{ opacity: 0, x: 16 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -16 }}
            className="mx-auto w-full max-w-[520px]"
          >
            <div className="glass-panel relative overflow-hidden rounded-[34px] border border-white/12 p-4 shadow-[0_30px_80px_rgba(0,0,0,0.38)]">
              <div className="relative grid gap-4 sm:grid-cols-[0.82fr_1fr]">
                <div className="relative overflow-hidden rounded-[28px] border border-white/12 bg-black/25">
                  <img src={movie.poster} alt={`${movie.title} poster`} className="h-full min-h-[25rem] w-full object-cover object-center" />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent" />
                  <div className="absolute inset-x-0 bottom-0 p-4 text-white">
                    <p className="text-[10px] uppercase tracking-[0.35em] text-white/58">Poster Stack</p>
                    <p className="mt-2 text-sm font-semibold">{movie.heroTag}</p>
                  </div>
                </div>

                <div className="flex flex-col gap-4">
                  <button
                    type="button"
                    onClick={onWatchTrailer}
                    className="overflow-hidden rounded-[28px] border border-white/12 bg-black/25 text-left"
                  >
                    <div className="relative">
                      <img src={movie.trailerThumbnail || movie.backdrop} alt={`${movie.title} trailer preview`} className="h-48 w-full object-cover object-center" />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/20 to-transparent" />
                      <div className="absolute inset-0 flex items-end justify-between p-4">
                        <div>
                          <p className="text-[10px] uppercase tracking-[0.35em] text-white/58">Trailer Preview</p>
                          <p className="mt-2 text-sm font-semibold text-white">{movie.trailerAvailable ? 'Play official trailer' : 'View trailer updates'}</p>
                        </div>
                        <span className="inline-flex size-12 items-center justify-center rounded-full border border-white/15 bg-black/45 text-white backdrop-blur-xl">
                          <PlayCircle className="size-5" style={{ color: 'var(--movie-accent)' }} />
                        </span>
                      </div>
                    </div>
                  </button>

                  <div className="rounded-[28px] border border-white/12 bg-white/8 p-5 backdrop-blur-2xl">
                    <div className="grid gap-4 sm:grid-cols-2">
                      <div className="rounded-2xl border border-white/10 bg-black/15 p-4">
                        <p className="text-xs uppercase tracking-[0.3em] text-white/52">Runtime</p>
                        <p className="mt-2 inline-flex items-center gap-2 text-lg font-semibold text-white">
                          <Clock3 className="size-4" />
                          {movie.duration}
                        </p>
                      </div>
                      <div className="rounded-2xl border border-white/10 bg-black/15 p-4">
                        <p className="text-xs uppercase tracking-[0.3em] text-white/52">Availability</p>
                        <p className="mt-2 text-lg font-semibold text-white">{movie.cities?.length ?? 0} cities live</p>
                      </div>
                    </div>

                    <div className="mt-5 space-y-3">
                      <div className="flex items-center justify-between text-[11px] uppercase tracking-[0.28em] text-white/48">
                        <span>{progressLabel}</span>
                        <span>{activeIndex + 1}/{progressTotal}</span>
                      </div>
                      <div className="h-2 overflow-hidden rounded-full bg-white/10">
                        <motion.div
                          key={movie.id}
                          initial={{ width: 0 }}
                          animate={{ width: `${progressValue}%` }}
                          className="h-full rounded-full shadow-[0_0_24px_var(--movie-accent)]"
                          style={{
                            background: 'linear-gradient(90deg, var(--movie-accent), color-mix(in srgb, var(--movie-primary) 70%, white))',
                          }}
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {canCycle ? (
                <div className="relative mt-4 flex flex-wrap gap-2">
                  {movies.slice(0, 5).map((item, index) => (
                    <button
                      key={item.id}
                      type="button"
                      onClick={() => onSelectMovie(index)}
                      className={`h-1.5 rounded-full transition ${index === activeIndex ? 'w-12 bg-white shadow-[0_0_16px_rgba(255,255,255,0.35)]' : 'w-6 bg-white/25 hover:bg-white/45'}`}
                      aria-label={`Show ${item.title}`}
                    />
                  ))}
                </div>
              ) : null}
            </div>
          </motion.div>
        </div>
      </section>
    </MotionConfig>
  )
}
