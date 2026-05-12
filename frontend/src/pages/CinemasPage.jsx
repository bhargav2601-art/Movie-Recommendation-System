import { MapPin, MonitorPlay, Sparkles } from 'lucide-react'
import { useEffect, useState } from 'react'

import { fetchMovies } from '../api/movies'
import { Card } from '../components/ui/card'


export function CinemasPage() {
  const [cities, setCities] = useState([])

  useEffect(() => {
    fetchMovies()
      .then((data) => {
        const summary = Array.from(
          data.items.reduce((acc, movie) => {
            movie.cities.forEach((city) => {
              const current = acc.get(city) ?? { city, movies: new Set(), languages: new Set() }
              current.movies.add(movie.title)
              movie.language.forEach((language) => current.languages.add(language))
              acc.set(city, current)
            })
            return acc
          }, new Map()).values(),
        ).map((item) => ({
          city: item.city,
          movieCount: item.movies.size,
          languageCount: item.languages.size,
        }))
        setCities(summary)
      })
      .catch(() => setCities([]))
  }, [])

  return (
    <section className="section-shell py-14">
      <h1 className="font-display text-4xl font-extrabold text-foreground">Cinemas</h1>
      <p className="mt-3 max-w-3xl text-muted">Explore active booking cities and the formats currently driving the strongest theatrical demand.</p>
      <div className="mt-8 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
        {cities.map((item) => (
          <Card key={item.city} className="p-6">
            <div className="flex items-center justify-between">
              <div className="inline-flex size-12 items-center justify-center rounded-2xl bg-neon/10 text-neon">
                <MapPin className="size-5" />
              </div>
              <span className="rounded-full border border-border/30 bg-card/55 px-3 py-1 text-xs uppercase tracking-[0.28em] text-muted">
                live
              </span>
            </div>
            <h2 className="mt-5 font-display text-3xl font-bold text-foreground">{item.city}</h2>
            <div className="mt-5 space-y-3 text-sm text-muted">
              <p className="inline-flex items-center gap-2">
                <MonitorPlay className="size-4 text-gold" />
                {item.movieCount} movies currently bookable
              </p>
              <p className="inline-flex items-center gap-2">
                <Sparkles className="size-4 text-neon" />
                {item.languageCount} language selections
              </p>
            </div>
          </Card>
        ))}
      </div>
    </section>
  )
}
