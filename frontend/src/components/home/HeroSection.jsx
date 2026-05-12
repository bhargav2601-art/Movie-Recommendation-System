import { useEffect, useState } from 'react'

import { CinematicHero } from '../cinematic/CinematicHero'
import { TrailerModal } from '../common/TrailerModal'

export function HeroSection({ movies = [] }) {
  const [active, setActive] = useState(0)
  const [showTrailer, setShowTrailer] = useState(false)

  useEffect(() => {
    if (!movies.length) return undefined
    const timer = window.setInterval(() => {
      setActive((value) => (value + 1) % movies.length)
    }, 5200)
    return () => window.clearInterval(timer)
  }, [movies])

  const featured = movies[active]

  if (!featured) return null

  return (
    <>
      <CinematicHero
        movie={featured}
        movies={movies}
        activeIndex={active}
        onSelectMovie={setActive}
        onWatchTrailer={() => setShowTrailer(true)}
        detailHref={`/movies/${featured.id}`}
      />
      <TrailerModal movie={featured} open={showTrailer} onClose={() => setShowTrailer(false)} />
    </>
  )
}
