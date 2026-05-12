import { CalendarClock, MapPin } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { fetchMovieDetails } from '../api/movies'
import { CinematicHero } from '../components/cinematic/CinematicHero'
import { MediaCarousel } from '../components/common/MediaCarousel'
import { TrailerModal } from '../components/common/TrailerModal'
import { CastCarousel } from '../components/movies/CastCarousel'
import { MovieShelf } from '../components/movies/MovieShelf'
import { Button } from '../components/ui/button'
import { Card } from '../components/ui/card'

export function MovieDetailsPage() {
  const { movieId } = useParams()
  const [movie, setMovie] = useState(null)
  const [showTrailer, setShowTrailer] = useState(false)

  useEffect(() => {
    fetchMovieDetails(movieId).then(setMovie)
  }, [movieId])

  if (!movie) {
    return <section className="section-shell py-20 text-muted">Loading movie details...</section>
  }

  return (
    <div className="pb-20">
      <CinematicHero
        movie={movie}
        activeIndex={0}
        onWatchTrailer={() => setShowTrailer(true)}
        minHeight="auto"
        progressLabel="Audience Momentum"
      />

      <section className="section-shell grid gap-8 py-14">
        <div className="grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
          <Card className="p-6">
            <p className="text-xs uppercase tracking-[0.35em] text-subtle">Storyline</p>
            <h2 className="mt-4 font-display text-3xl font-bold text-foreground">Why this one plays big on the big screen</h2>
            <p className="mt-4 text-sm leading-8 text-muted">{movie.whyRecommended || movie.storyline}</p>
            <div className="mt-6 flex flex-wrap gap-2">
              {movie.subtitles?.map((item) => (
                <span key={item} className="rounded-full border border-border/30 bg-card/55 px-3 py-2 text-xs text-muted">
                  {item} subtitles
                </span>
              ))}
            </div>
          </Card>

          <Card className="p-6">
            <p className="text-xs uppercase tracking-[0.35em] text-subtle">Release Info</p>
            <div className="mt-5 grid gap-4 sm:grid-cols-2">
              {[
                ['Language', movie.language.join(' • ')],
                ['Runtime', movie.duration],
                ['Release Date', movie.releaseDate],
                ['Mood', movie.mood],
              ].map(([label, value]) => (
                <div key={label} className="rounded-2xl border border-border/30 bg-card/55 p-4">
                  <p className="text-subtle">{label}</p>
                  <p className="mt-2 text-sm font-semibold text-foreground">{value}</p>
                </div>
              ))}
            </div>
          </Card>
        </div>

        <Card className="p-6">
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="text-xs uppercase tracking-[0.35em] text-subtle">Gallery</p>
              <h2 className="mt-3 font-display text-3xl font-bold text-foreground">Still frames and cinematic highlights</h2>
            </div>
            <Button variant="secondary" onClick={() => setShowTrailer(true)}>
              Watch Trailer
            </Button>
          </div>
          <div className="mt-6">
            <MediaCarousel items={movie.gallery} title={movie.title} />
          </div>
        </Card>

        <Card className="p-6">
          <p className="text-xs uppercase tracking-[0.35em] text-subtle">Cast</p>
          <h2 className="mt-3 font-display text-3xl font-bold text-foreground">Featured cast lineup</h2>
          <div className="mt-6">
            <CastCarousel cast={movie.cast} />
          </div>
        </Card>

        <Card className="p-6">
          <p className="text-xs uppercase tracking-[0.35em] text-subtle">Showtimes</p>
          <h2 className="mt-3 font-display text-3xl font-bold text-foreground">Nearby cinemas and live show windows</h2>
          <div className="mt-6 space-y-4">
            {movie.theaters.map((theater) => (
              <div key={theater.id} className="rounded-3xl border border-border/30 bg-card/45 p-5">
                <div className="grid gap-5 lg:grid-cols-[1.1fr_0.9fr]">
                  <div>
                    <div className="flex flex-wrap items-center gap-3">
                      <p className="font-display text-2xl font-bold text-foreground">{theater.name}</p>
                      <span className="rounded-full border border-border/30 bg-card/55 px-3 py-1 text-xs text-neon">
                        {theater.chain}
                      </span>
                    </div>
                    <div className="mt-3 flex flex-wrap gap-4 text-sm text-muted">
                      <span className="inline-flex items-center gap-2">
                        <MapPin className="size-4 text-neon" />
                        {theater.location}, {theater.city}
                      </span>
                      <span>{theater.distance} km away</span>
                      <span>{theater.ratings} / 5</span>
                    </div>
                    <div className="mt-4 flex flex-wrap gap-2">
                      {theater.formats.map((format) => (
                        <span key={format} className="rounded-full border border-gold/20 bg-gold/10 px-3 py-2 text-xs text-gold">
                          {format}
                        </span>
                      ))}
                    </div>
                    <div className="mt-4 flex flex-wrap gap-2">
                      {theater.facilities.map((facility) => (
                        <span key={facility} className="rounded-full border border-border/30 bg-card/55 px-3 py-2 text-xs text-muted">
                          {facility}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="space-y-3">
                    {theater.screensList.map((screen) => (
                      <div key={screen.screenName} className="rounded-2xl border border-border/30 bg-background-soft/55 p-4">
                        <p className="font-semibold text-foreground">{screen.screenName}</p>
                        <p className="mt-1 text-xs uppercase tracking-[0.25em] text-subtle">
                          {screen.formats.join(' • ')}
                        </p>
                        <div className="mt-3 flex flex-wrap gap-2">
                          {screen.timings.map((timing) => (
                            <Link key={timing.showId} to={`/booking/${timing.showId}`}>
                              <Button variant="secondary">
                                <CalendarClock className="mr-2 size-4" />
                                {timing.showDate} • {timing.showTime}
                              </Button>
                            </Link>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </section>

      <section className="section-shell mt-6">
        <h2 className="font-display text-3xl font-bold text-foreground">Similar Movies</h2>
        <div className="mt-6">
          <MovieShelf movies={movie.similar} compact autoSlide={false} />
        </div>
      </section>

      <TrailerModal movie={movie} open={showTrailer} onClose={() => setShowTrailer(false)} />
    </div>
  )
}
