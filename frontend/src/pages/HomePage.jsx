import { useEffect, useState } from 'react'

import { fetchMovieMeta, fetchRecommendations } from '../api/movies'
import { FilterChips } from '../components/common/FilterChips'
import { SearchBar } from '../components/common/SearchBar'
import { SectionHeader } from '../components/common/SectionHeader'
import { HeroSection } from '../components/home/HeroSection'
import { MovieShelf } from '../components/movies/MovieShelf'


const emptySections = {
  hero: [],
  trending: [],
  recommended: [],
  topRated: [],
  trendingInCity: [],
  scifi: [],
  action: [],
  romance: [],
  horror: [],
  comingSoon: [],
  imaxExperience: [],
  familyMovies: [],
}


export function HomePage() {
  const [search, setSearch] = useState('')
  const [city, setCity] = useState('')
  const [genre, setGenre] = useState('')
  const [meta, setMeta] = useState({ genres: [], cities: [], formats: [] })
  const [sections, setSections] = useState(emptySections)

  useEffect(() => {
    async function load() {
      const [metaData, recommendationData] = await Promise.all([
        fetchMovieMeta(),
        fetchRecommendations(city),
      ])
      setMeta(metaData)

      const filterMovies = (items = []) =>
        items.filter((movie) => {
          const searchOkay = search ? movie.title.toLowerCase().includes(search.toLowerCase()) : true
          const genreOkay = genre ? movie.genre.includes(genre) : true
          return searchOkay && genreOkay
        })

      setSections(
        Object.fromEntries(
          Object.entries(recommendationData).map(([key, value]) => [key, filterMovies(value)]),
        ),
      )
    }

    load()
  }, [city, genre, search])

  const shelves = [
    ['trending', 'Trending Now', 'The movies everybody is opening the app for right now.', false],
    ['topRated', 'Top Rated', 'Critics, audiences, and repeat watch behavior all pointing the same way.', false],
    ['recommended', 'Recommended', 'A recommendation row tuned for booking intent, not passive scrolling.', true],
    ['scifi', 'Sci-Fi', 'World-building, giant-format imagery, and event-level spectacle.', true],
    ['action', 'Action', 'Hero entries, spy chaos, and high-velocity theatrical payoffs.', true],
    ['romance', 'Romance', 'Sweeping chemistry, heartbreak, and modern big-screen love stories.', true],
    ['horror', 'Horror', 'Tension, folklore, dread, and crowd reactions worth hearing in a theater.', true],
    ['comingSoon', 'Coming Soon', 'The next wave of theatrical hype, queued up early.', true],
    ['imaxExperience', 'IMAX Experience', 'Large-format favorites built for booming sound and towering imagery.', false],
    ['familyMovies', 'Family Movies', 'Warm, all-ages crowd pleasers for group bookings.', true],
  ]

  return (
    <div className="pb-24">
      <HeroSection movies={sections.hero.length ? sections.hero : sections.trending} />

      <section className="section-shell relative z-10 -mt-14">
        <div className="glass-panel rounded-[34px] p-4 md:p-6">
          <div className="grid gap-4 lg:grid-cols-[1.5fr_0.8fr]">
            <SearchBar value={search} onChange={setSearch} />
            <select
              value={city}
              onChange={(event) => setCity(event.target.value)}
              className="select-theme"
            >
              <option value="">All Cities</option>
              {meta.cities.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </div>
          <div className="mt-4">
            <FilterChips items={meta.genres} value={genre} onChange={setGenre} />
          </div>
        </div>
      </section>

      {shelves.map(([key, title, description, compact]) =>
        sections[key]?.length ? (
          <section key={key} className="section-shell mt-16">
            <SectionHeader eyebrow={title} title={title} description={description} />
            <MovieShelf movies={sections[key]} compact={compact} />
          </section>
        ) : null,
      )}
    </div>
  )
}
