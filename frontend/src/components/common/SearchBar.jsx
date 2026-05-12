import { Search } from 'lucide-react'
import { useEffect, useState } from 'react'

import { fetchSearchSuggestions } from '../../api/movies'
import { Input } from '../ui/input'

export function SearchBar({ value, onChange }) {
  const [suggestions, setSuggestions] = useState([])

  useEffect(() => {
    const timer = window.setTimeout(async () => {
      try {
        const data = await fetchSearchSuggestions(value)
        setSuggestions(data.items)
      } catch {
        setSuggestions([])
      }
    }, 220)

    return () => window.clearTimeout(timer)
  }, [value])

  return (
    <div className="relative">
      <Search className="pointer-events-none absolute left-4 top-1/2 size-4 -translate-y-1/2 text-subtle" />
      <Input
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder="Search films, stars, languages, or experiences"
        className="pl-11"
      />
      {value && suggestions.length > 0 ? (
        <div className="glass-panel absolute left-0 right-0 top-[calc(100%+0.75rem)] z-20 rounded-2xl p-2">
          {suggestions.map((item) => (
            <button
              key={item}
              onClick={() => onChange(item)}
              className="block w-full rounded-xl px-3 py-2 text-left text-sm text-muted transition hover:bg-card/70 hover:text-foreground"
            >
              {item}
            </button>
          ))}
        </div>
      ) : null}
    </div>
  )
}
