import { useEffect, useState } from 'react'

import { fetchMovieMeta, fetchMovies } from '../api/movies'
import { FilterChips } from '../components/common/FilterChips'
import { SearchBar } from '../components/common/SearchBar'
import { SectionHeader } from '../components/common/SectionHeader'
import { MovieCard } from '../components/movies/MovieCard'

export function BrowsePage() {
  const [movies, setMovies] = useState([])
  const [meta, setMeta] = useState({ genres: [], languages: [], cities: [] })
  const [filters, setFilters] = useState({
    search: '',
    genre: '',
    language: '',
    city: '',
    sort: 'trending',
  })

  useEffect(() => {
    fetchMovieMeta().then(setMeta)
  }, [])

  useEffect(() => {
    fetchMovies(filters).then((data) => setMovies(data.items))
  }, [filters])

  return (
    <section className="section-shell py-14">
      <SectionHeader
        eyebrow="Movie Library"
        title="Browse premium theatrical experiences"
        description="Filter by language, genre, city, and recommendation strength with a discovery layout tuned for both desktop and mobile."
      />

      <div className="glass-panel rounded-[30px] p-4 md:p-6">
        <div className="grid gap-4 lg:grid-cols-4">
          <div className="lg:col-span-2">
            <SearchBar
              value={filters.search}
              onChange={(value) => setFilters((prev) => ({ ...prev, search: value }))}
            />
          </div>
          <select
            value={filters.language}
            onChange={(event) => setFilters((prev) => ({ ...prev, language: event.target.value }))}
            className="select-theme"
          >
            <option value="">All Languages</option>
            {meta.languages.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
          <select
            value={filters.city}
            onChange={(event) => setFilters((prev) => ({ ...prev, city: event.target.value }))}
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

        <div className="mt-4 flex flex-col gap-4">
          <FilterChips
            items={meta.genres}
            value={filters.genre}
            onChange={(value) => setFilters((prev) => ({ ...prev, genre: value }))}
          />
          <div className="flex flex-wrap gap-2">
            {[
              ['trending', 'Trending'],
              ['rating', 'Top Rated'],
              ['release', 'Latest'],
            ].map(([value, label]) => (
              <button
                key={value}
                onClick={() => setFilters((prev) => ({ ...prev, sort: value }))}
                className={`rounded-full px-4 py-2 text-sm transition ${
                  filters.sort === value ? 'pill-button pill-button-active' : 'pill-button'
                }`}
              >
                {label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="mt-10 grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {movies.map((movie) => (
          <MovieCard key={movie.id} movie={movie} />
        ))}
      </div>
    </section>
  )
}
