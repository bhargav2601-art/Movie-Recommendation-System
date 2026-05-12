import { AnimatePresence, motion } from 'framer-motion'
import { ExternalLink, PlayCircle, X } from 'lucide-react'
import { Suspense, lazy, useEffect, useMemo, useState } from 'react'

import { normalizeTrailerUrl } from '../../lib/utils'

const ReactPlayer = lazy(() => import('react-player'))

function buildTrailerSources(movie) {
  const candidates = [
    movie?.trailerWatchUrl,
    movie?.trailerUrl,
    ...(movie?.trailerVariants ?? []).flatMap((item) => [item?.trailerWatchUrl, item?.trailerUrl]),
  ].filter(Boolean)

  const unique = []
  for (const source of candidates) {
    if (!unique.includes(source)) unique.push(source)
  }
  return unique
}

export function TrailerModal({ movie, open, onClose }) {
  const trailerSources = useMemo(() => buildTrailerSources(movie), [movie])
  const [sourceIndex, setSourceIndex] = useState(0)
  const [mode, setMode] = useState('player')

  const currentSource = trailerSources[sourceIndex] || ''
  const fallbackEmbedSource = normalizeTrailerUrl(trailerSources[sourceIndex + 1] || trailerSources[0] || '')
  const hasTrailer = Boolean(movie?.trailerAvailable && trailerSources.length)
  const trailerVisual = movie?.trailerThumbnail || movie?.backdrop || movie?.poster

  useEffect(() => {
    if (!open) return undefined

    setSourceIndex(0)
    setMode('player')

    const handleKeyDown = (event) => {
      if (event.key === 'Escape') onClose()
    }

    window.addEventListener('keydown', handleKeyDown)
    document.body.style.overflow = 'hidden'
    return () => {
      window.removeEventListener('keydown', handleKeyDown)
      document.body.style.overflow = ''
    }
  }, [open, onClose, movie?.id])

  const moveToNextSource = () => {
    if (sourceIndex < trailerSources.length - 1) {
      setSourceIndex((current) => current + 1)
      setMode('player')
      return
    }

    if (fallbackEmbedSource && mode === 'player') {
      setMode('iframe')
      return
    }

    setMode('poster')
  }

  const renderPlayer = () => {
    if (!hasTrailer || mode === 'poster') {
      return (
        <div className="relative flex h-full w-full items-end overflow-hidden">
          <img src={trailerVisual} alt={movie?.title} className="absolute inset-0 h-full w-full object-cover opacity-70" />
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.08),transparent_28%),linear-gradient(180deg,rgba(3,6,16,0.3),rgba(3,6,16,0.9))]" />
          <div className="relative z-10 max-w-2xl p-8">
            <p className="text-xs uppercase tracking-[0.35em] text-subtle">
              {hasTrailer ? 'Trailer Playback Fallback' : 'Official Trailer Pending'}
            </p>
            <h3 className="mt-3 font-display text-3xl font-bold text-foreground">{movie?.title}</h3>
            <p className="mt-3 text-sm leading-7 text-muted">
              {hasTrailer
                ? 'Embedded playback was blocked, so we switched to a safe poster fallback with a direct YouTube handoff.'
                : 'No official trailer is available yet. CineVerse keeps the modal cinematic without showing unrelated or broken footage.'}
            </p>
            {movie?.trailerWatchUrl ? (
              <a
                href={movie.trailerWatchUrl}
                target="_blank"
                rel="noreferrer"
                className="mt-5 inline-flex items-center gap-2 rounded-full border border-border/30 bg-card/60 px-4 py-3 text-sm font-semibold text-foreground transition hover:bg-card/85"
              >
                <ExternalLink className="size-4" />
                Open on YouTube
              </a>
            ) : null}
          </div>
        </div>
      )
    }

    if (mode === 'iframe' && fallbackEmbedSource) {
      return (
        <iframe
          key={fallbackEmbedSource}
          className="h-full w-full"
          src={`${fallbackEmbedSource}?autoplay=1&mute=1&rel=0&playsinline=1`}
          title={`${movie?.title} trailer fallback`}
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          allowFullScreen
        />
      )
    }

    return (
      <Suspense fallback={<div className="h-full w-full bg-black/50" />}>
        <ReactPlayer
          key={currentSource}
          src={currentSource}
          playing
          muted
          controls
          playsInline
          width="100%"
          height="100%"
          onError={moveToNextSource}
          config={{
            youtube: {
              playerVars: {
                autoplay: 1,
                mute: 1,
                rel: 0,
                playsinline: 1,
              },
            },
          }}
        />
      </Suspense>
    )
  }

  return (
    <AnimatePresence>
      {open ? (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-[100] bg-overlay/85 backdrop-blur-xl"
        >
          <button className="absolute inset-0" onClick={onClose} aria-label="Close trailer" />
          <div className="section-shell relative flex min-h-screen items-center justify-center py-10">
            <motion.div
              initial={{ opacity: 0, y: 24, scale: 0.96 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 18, scale: 0.98 }}
              className="glass-panel relative w-full max-w-6xl overflow-hidden rounded-[34px]"
            >
              <div className="absolute inset-x-0 top-0 z-10 flex items-center justify-between bg-gradient-to-b from-overlay/80 to-transparent p-5">
                <div className="flex items-center gap-3">
                  <div className="rounded-full bg-neon/15 p-3 text-neon">
                    <PlayCircle className="size-5" />
                  </div>
                  <div>
                    <p className="text-xs uppercase tracking-[0.35em] text-subtle">Now Playing</p>
                    <h2 className="font-display text-2xl font-bold text-foreground">{movie?.title}</h2>
                  </div>
                </div>
                <button
                  onClick={onClose}
                  className="rounded-full border border-border/30 bg-card/55 p-3 text-muted transition hover:bg-card/80 hover:text-foreground"
                >
                  <X className="size-5" />
                </button>
              </div>

              <div className="relative aspect-video bg-overlay">
                {renderPlayer()}
                <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-overlay/40 via-transparent to-overlay/10" />
              </div>

              <div className="grid gap-4 border-t border-border/30 bg-card/35 p-5 md:grid-cols-[1fr_auto] md:items-center">
                <p className="text-sm leading-7 text-muted">
                  {mode === 'player'
                    ? 'Premium trailer playback with automatic source fallback, autoplay, and fullscreen support.'
                    : 'When embeds are blocked, CineVerse falls back gracefully so the trailer flow never dead-ends.'}
                </p>
                <a
                  href={movie?.trailerWatchUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="rounded-full border border-border/30 bg-card/55 px-4 py-3 text-sm font-semibold text-muted transition hover:bg-card/80 hover:text-foreground"
                >
                  {hasTrailer ? 'Open on YouTube' : 'Check YouTube'}
                </a>
              </div>
            </motion.div>
          </div>
        </motion.div>
      ) : null}
    </AnimatePresence>
  )
}
