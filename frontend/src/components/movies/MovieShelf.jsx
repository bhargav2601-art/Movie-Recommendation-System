import { ChevronLeft, ChevronRight } from 'lucide-react'
import { useEffect, useRef } from 'react'

import { MovieCard } from './MovieCard'


export function MovieShelf({ movies = [], compact = false, autoSlide = true }) {
  const railRef = useRef(null)

  const scrollByCards = (direction) => {
    const rail = railRef.current
    if (!rail) return
    const width = compact ? 286 : 344
    rail.scrollBy({ left: direction * width, behavior: 'smooth' })
  }

  useEffect(() => {
    if (!autoSlide || movies.length < 5) return undefined
    const timer = window.setInterval(() => {
      const rail = railRef.current
      if (!rail) return
      const reachedEnd = rail.scrollLeft + rail.clientWidth >= rail.scrollWidth - 24
      rail.scrollTo({
        left: reachedEnd ? 0 : rail.scrollLeft + (compact ? 286 : 344),
        behavior: 'smooth',
      })
    }, 4200)
    return () => window.clearInterval(timer)
  }, [autoSlide, compact, movies.length])

  return (
    <div className="relative">
      <div className="absolute right-0 top-[-4.75rem] hidden items-center gap-2 md:flex">
        <button
          type="button"
          onClick={() => scrollByCards(-1)}
          className="glass-button inline-flex size-11 items-center justify-center text-muted hover:text-foreground"
        >
          <ChevronLeft className="size-5" />
        </button>
        <button
          type="button"
          onClick={() => scrollByCards(1)}
          className="glass-button inline-flex size-11 items-center justify-center text-muted hover:text-foreground"
        >
          <ChevronRight className="size-5" />
        </button>
      </div>

      <div ref={railRef} className="flex gap-5 overflow-x-auto pb-4 pt-1 movie-rail snap-x snap-mandatory">
        {movies.map((movie) => (
          <div key={movie.id} className={`shrink-0 snap-start ${compact ? 'w-[270px]' : 'w-[328px]'}`}>
            <MovieCard movie={movie} compact={compact} />
          </div>
        ))}
      </div>
    </div>
  )
}
